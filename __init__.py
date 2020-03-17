# import libraries
from mycroft import MycroftSkill, intent_file_handler, intent_handler, \
                    AdaptIntent
from mycroft.util.log import LOG
import requests
import time
import urllib3
from bs4 import BeautifulSoup

# specify the url
URL = ‘https://medlineplus.gov/'
PAGE = requests.get (URL)
SOUP = BeautifulSoup (page.content, 'html.parser')
SUMMARY = soup.find(id='summary-title')

class MedlinePlusSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.is_reading = False
	    @intent_file_handler('medlineplus.intent')
    def handle_medlineplus(self, message):
        if message.data.get("SUMMARY") is None:
            response = self.get_response('medlineplus', num_retries=0)
            if response is None:
                return
        else:
            response = message.data.get("SUMMARY")
        self.speak_dialog('searching.dialog', data={"SUMMARY": response})
        index = self.get_index("https://medlineplus.gov/")
        result = match_one(response, list(index.keys()))

        if result[1] < 0.8:
            self.speak_dialog('clarify.dialog', data={"SUMMARY": result[0]})
            response = self.ask_yesno('is_it')
            if response != 'yes':
                self.speak_dialog('found.dialog')
                return
        self.speak_dialog('Here_is_the_summary_on', data={"SUMMARY": result[0]})
        # self.log.info(result + " " + result[0])
        self.settings['SUMMARY'] = result[0]
        time.sleep(3)
        self.tell_SUMMARY(index.get(result[0]), 0)

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

    def get_SUMMARY(self, url):
        soup = self.get_soup(url)
        lines = [a.text.strip() for a in soup.find(id='summary-title')
        return lines

def create_skill():
    return MedlinePlusSkill()
