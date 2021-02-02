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
import urllib
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import xml.etree.ElementTree

class MedlinePlus(MycroftSkill):
    def __init__(self):
        super(MedlinePlusSkill, self).__init__(name="MedlinePlusSkill")
    # Initialize working variables used within the skill.
    def initialize(self):
        self.is_reading = False
    
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

base_url = 'https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term='
ret_type = '&rettype=brief'

def MedlinePlus_query(search_terms):
    term = "{0}".format(search_terms)
    term = urllib.quote(term)
    results = []
    url = (base_url + term + ret_type)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    for document in soup.findAll('document'):
        contents = document.findAll('content')
        for content in contents:
            if content.get('name') == 'title':
                taggedTitle = content.string
                title = strip_tags(taggedTitle)
            if content.get('name') == 'snippet':
                taggedSnippet = content.string
                snippet = strip_tags(taggedSnippet)
                snippet = strip_tags(snippet)
            if content.get('name') == 'FullSummary':
                taggedSummary = content.string
                summary = strip_tags(taggedSummary)
        
        results.append({
            'title': remove_tags(title),
            'link': document.get('url'),
            'summary': remove_tags(snippet),
            'content': remove_tags(summary),
            'from': 'From:     MedlinePlus'
        })

    return results

def create_skill():
    return MedlinePlusSkill()
