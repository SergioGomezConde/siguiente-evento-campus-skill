from mycroft import MycroftSkill, intent_file_handler


class SiguienteEventoCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.evento.siguiente.intent')
    def handle_campus_evento_siguiente(self, message):
        self.speak_dialog('campus.evento.siguiente')


def create_skill():
    return SiguienteEventoCampus()

