"""
skill medlineplus
Copyright (C) 2020 TheNurse

This program is free software: you can redistribute it and/or modify
it under the summarys of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.audio import wait_while_speaking
import xml.etree.ElementTree as xml
import requests
import time

# https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=full-summary:<search term>&retmax=1

link = "https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=full-summary:{term}&retmax=1".format(
        nlmSearchResult
    )

class medlineplusSkill(MycroftSkill):
	def __init__(self):
		super(medlineplusSkill, self).__init__(name="medlineplusSkill")

	@intent_handler(IntentBuilder("").require("medlineplus").
		require("FullSummary"))
	def handle_intent(self, message):
	# Extract what the user asked about
	elf._lookup(message.data.get("FullSummary"))

	def _lookup(self, search):
	try:
		# the base url is https://wsearch.nlm.nih.gov/ws/query
		# Talk to the user, as this can take a little time...
		self.speak_dialog("searching", {"term": search})

		# First step is to get the xml search results.  
		# results come back in a specific format
		results = web.search(search, 1)
		if len(results) == 0:
		self.speak_dialog("no entry found")
		return
            
		except web.exceptions.DisambiguationError as e:
		# Test:  "tell me about Coronary Artery Disease"
		options = e.options[:5]

		option_list = (", ".join(options[:-1]) + " " +
			self.translate("or") + " " + options[-1])
			choice = self.get_response('disambiguate',
			data={"options": option_list})
			if choice:
			self._lookup(choice)

		except Exception as e:
		LOG.error("Error: {0}".format(e))
        
		try:
		self._lookup(search)
		except PageError:
		self._lookup(search, auto_suggest=False)
		except Exception as e:
		self.log.error("Error: {0}".format(e))

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
            
   
		lines = self.get_item(url)
		for line in lines[bookmark:]:
		
		time.sleep(.5)
	if self.is_reading is False:
		break
		sentences = line.split('. ')
		for sentens in sentenses:
		if self.is_reading is False:
		break
		else:
		wait_while_speaking()
		self.speak(sentens, wait=True)
	if self.is_reading is True:
		self.is_reading = False
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

	def get_item(self, url):
		e = xml.etree.ElementTree.fromstring(response)
		for doc in e.iter('document'):
		title = ''
		summary = ''
		for content in doc.iter('content'):
		if content.get('name') == 'title':
		title = content.text
		elif content.get('name') == 'FullSummary':
		summary = content.text
        
       
	def remove_tags(text):
	return ''.join(xml.etree.ElementTree.fromstring("<dummy_tag>" + text +"</dummy_tag>").itertext())

def medlinePlus_query(search_terms):
	# Specify the base
	root_url = 'https://wsearch.nlm.nih.gov/ws/query'
	term_delimiter = '+'
	keywords = term_delimiter.join(search_terms.split(' '))

	search_url = '%s?db=%s&term="%s"' % (root_url, 'healthTopics', keywords)

	# Create our results list which we'll populate.
	results = []

	try:
	# Connect to the server and read the response generated.
	response = urllib2.urlopen(search_url).read()

	e = xml.etree.ElementTree.fromstring(response)
	for doc in e.iter('document'):
	title = ''#800080
	summary = ''
	for content in doc.iter('content'):
	if content.get('name') == 'title':
	title = content.text
	elif content.get('name') == 'FullSummary':
	summary = content.text

	entry = {
	'title': remove_tags(title),
	'link': doc.get('url'),
	'summary': remove_tags(summary)
	}

	results.append(entry)


def create_skill():
	return medlineplusSkill()
