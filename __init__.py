import json
import os

from mycroft import MycroftSkill, intent_file_handler

# Fichero JSON donde almacenar la informacion
ficheroJSON = "/home/serggom/scraping/datos.json"


class SiguienteEventoCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.evento.siguiente.intent')
    def handle_campus_evento_siguiente(self, message):

        if os.path.exists(ficheroJSON):

            # Lectura de la informacion del fichero JSON
            with open(ficheroJSON) as ficheroEventos:
                data = json.load(ficheroEventos)
                if len(data['eventos']) > 0:
                    event = data['eventos'][0]
                    self.speak("El " + event['fecha'] + " a las " + event['hora'] + " tienes " + event['nombre'])
                else:
                    self.speak("No existen eventos próximos")

        else:
            self.speak("Lo siento, no dispongo de esa información")


def create_skill():
    return SiguienteEventoCampus()
