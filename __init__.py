from mycroft import MycroftSkill, intent_file_handler


class MedlinePlus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('plus.medline.intent')
    def handle_plus_medline(self, message):
        self.speak_dialog('plus.medline')


def create_skill():
    return MedlinePlus()

