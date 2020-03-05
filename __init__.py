from mycroft import MycroftSkill, intent_file_handler, intent_handler, \
                    AdaptIntent
from mycroft.util.log import LOG
import requests
import metapub

BASE_URL = 'https://wsearch.nlm.nih.gov/ws/query?
SEARCH = URL +db=healthTopics&term={title}&rettype=brief&retstart=0&retmax=1


def search_medlineplus(title):
    r = requests.get(SEARCH, params={'s': title})
        else:
        return None
    }
 class MedlinePlus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
         @intent_file_handler('plus.medline.intent')
    def handle_plus_medline(self, message):
        self.speak_dialog('plus.medline')

        title = search_medline(message.data['title'])
        if title:
            self.speak_dialog('This is what I found', {
                time.sleep(1)
            self.speak(['FullSummary'])
            self.set_context('brief', str((FullSummary)))
        else:
            self.speak_dialog('NotFound')

   @intent_file_handler('Needed.intent')
    def get_healthTopics(self, message):     
		                      
def create_skill():
    return MedlinePlus()
