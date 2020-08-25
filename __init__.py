"""
skill medlineplus
Copyright (C) 2020  TheNurse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
import requests
from bs4 import BeautifulSoup
import time


class Medlineplus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.is_reading = False

    @intent_file_handler('medlineplus.intent')
    def handle_medlineplus(self, message):
        if message.data.get("item") is None:
            response = self.get_response('medlineplus', num_retries=0)
            if response is None:
                return
        else:
            response = message.data.get("item")
        self.speak_dialog('let_me_find', data={"item": response})
        index = self.get_index("https://medlineplus.gov/all_healthtopics.html")
        result = match_one(response, list(index.keys()))

        if result[1] < 0.8:
            self.speak_dialog('that_would_be', data={"item": result[0]})
            response = self.ask_yesno('is_it_that')
            if response != 'yes':
                self.speak_dialog('no_item')
                return
        self.speak_dialog('i_know_that', data={"item": result[0]})
        # self.log.info(result + " " + result[0])
        self.settings['item'] = result[0]
        time.sleep(3)
        self.tell_item(index.get(result[0]), 0)

    @intent_file_handler('continue.intent')
    def handle_continue(self, message):
        if self.settings.get('item') is None:
            self.speak_dialog('no_item_to_continue')
        else:
            item = self.settings.get('item')
            self.speak_dialog('continue', data={"item": item})
            index = self.get_index("https://medlineplus.gov/all_healthtopics.html")
            self.tell_item(index.get(item), self.settings.get('bookmark') - 1)

    def tell_item(self, url, bookmark):
        self.is_reading = True
        self.settings['bookmark'] = bookmark
        if bookmark == 0:
            title = self.get_title(url)
            author = self.get_author(url)
            self.speak_dialog('title_by_author', data={'title': title, 'author': author})
            time.sleep(1)
        lines = self.get_item(url)
        for line in lines[bookmark:]:
            self.settings['bookmark'] += 1
            time.sleep(.5)
            if self.is_reading is False:
                break
            sentenses = line.split('. ')
            for sentens in sentenses:
                if self.is_reading is False:
                    break
                else:
                    wait_while_speaking()
                    self.speak(sentens, wait=True)
        if self.is_reading is True:
            self.is_reading = False
            self.settings['bookmark'] = 0
            self.settings['item'] = None
            time.sleep(2)
            self.speak_dialog('from_medlineplus')

    def stop(self):
        self.log.info('stop is called')
        if self.is_reading is True:
            self.is_reading = False
            return True
        else:
            return False

    def get_soup(self, url):
        try:
            return BeautifulSoup(requests.get(url).text, "html.parser")
        except Exception as SockException:
            self.log.error(SockException)

    def get_item(self, url):
        soup = self.get_soup(url)
        lines = [a.text.strip() for a in soup.find(id="item").find_all("p")[1:]]
        lines = [l for l in lines if not l.startswith("{") and not l.endswith("}")]
        return lines

    def get_title(self, url):
        soup = self.get_soup(url)
        title = [a.text.strip() for a in soup.findAll("item")][0]
        return title

    def get_author(self, url):
        soup = self.get_soup(url)
        author = [a.text.strip() for a in soup.findAll("div", {"class": "item"})][0]
        return str(author).split("  ")[0]

    def get_index(self, url):
        soup = self.get_soup(url)
        index = {}
        for link in soup.find(id="main").find_all('a'):
            index.update({link.text[2:]: link.get("href")})
        return index


def create_skill():
    return Medlineplus
