# import libraries
from mycroft import MycroftSkill, intent_file_handler, intent_handler, \
                    AdaptIntent
from mycroft.util.log import LOG
import requests
import time
import urllib3
from bs4 import BeautifulSoup

# specify the url
url = ‘https://medlineplus.gov/'
response = requests.get(url)
content = BeautifulSoup(page.content, 'html.parser')
summary = content.findAll('p', attrs={"class": "syndicate"}).text

class MedlinePlusSkill(MycroftSkill):
    def __init__(self):
        super(MedlinePlusSkill, self).__init__(name="MedlinePlusSkill")

    def initialize(self):
        self.is_reading = False
        
	@intent_handler(IntentBuilder("").require("Medline").require("Search"))
    def handle_medlineplus_intent(self, message):
		self.speak_dialog("found")
		 
        if message.data.get("summary") is None:
            response = self.get_response('notfound', num_retries=0)
            if response is None:
                return

	def get_soup(self, url):
        try:
            return BeautifulSoup(requests.get(url).text, "html.parser")
        except Exception as SockException:
            self.log.error(SockException)

    def get_summary(self, url):
        soup = self.get_soup(url)
        lines = [a.text.strip() for a in soup.find(id='summary-title')
        return lines
        
	def stop(self):
        self.log.info('stop is called')
        if self.is_reading is True:
            self.is_reading = False
            return True
        else:
            return False

def create_skill():
    return MedlinePlusSkill()
