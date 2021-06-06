"""
skill medlineplus
Copyright (C) 2021 The Nurse
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# import libraries

from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
import requests
from bs4 import BeautifulSoup
from mycroft import MycroftSkill, intent_handler


class MedlinePlusSkill(MycroftSkill):

    @intent_handler("medline.intent")
    def handle_medlineplus_intent(self, message):
        topic = message.data.get("topic")
        self.speak_dialog("let_me_find", {"disease": topic})
        # medlineplus refers to the topic-summary defined by the disease on medlineplus.gov
        if topic is None:
            response = self.get_response('notfound', num_retries=0)
            if response is None:
                return
            else:
                self.speak_dialog('found', data={"disease": topic})
        else:
            try:
                url = "https://medlineplus.gov/{disease}.html"
                html_content = requests.get(url).text
                soup = BeautifulSoup(html_content, "html5lib")
                main_class = soup.find("div",id="topic-summary")
                link = main_class.find("a")
                res = main_class.text
                self.result.append(str(res))
            except:
                pass

def create_skill():
    return MedlinePlusSkill()