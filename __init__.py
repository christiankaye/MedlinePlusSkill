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
from mycroft.util.parse imMedlinePlusSkill-masterport match_one
from mycroft.audio import wait_while_speaking
import requests
import time
import urllib
import xml.etree.ElementTree

class MedlinePlus(MycroftSkill):
    def __init__(self):
    super(MedlinePlusSkill, self).__init__(name="MedlinePlusSkill")
    
    # Initialize working variables used within the skill.
    self.count = 0
    
   @intent_handler(IntentBuilder().require("MedlinePlus"))
    def handle_medlineplus_intent(self, message):
        self.speak_dialog("let_me_find")
        # medlineplus refers to the summary defined by the disease on medlineplus.gov
			if message.data.get("MedlinePlus") is None:
            response = self.get_response('notfound', num_retries=0)
            if response is None:
               return
         else:
            response = message.data.get("MedlinePlus")
        self.speak_dialog('found', data={"FullSummary": response}) 

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
        response = urllib.urlopen(search_url).read()
        print (search_url) 
        e = xml.etree.ElementTree.fromstring(response)
        for doc in e.iter('document'):
            title = ''
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
        #print response 
        #print search_url   

    # Catch a URLError exception - something went wrong when connecting!
    except urllib.URLError as e:
        print ("Error when querying the MedlinePlus API: "), e

    # Return the list of results to the calling function.
    #print results
    return results

def create_skill():
    return MedlinePlusSkill()
