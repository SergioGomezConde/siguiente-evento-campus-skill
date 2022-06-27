from lib2to3.pgen2 import driver
import json

from mycroft import MycroftSkill, intent_file_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import date

# Fichero JSON donde almacenar la informacion
ficheroJSON = "/home/serggom/data.json"
informacion = {'asignaturas': [], 'usuario': [], 'eventos': [], 'siguiente_evento': [], 'mensajes': []}

def inicio_sesion(self):
    # Datos de acceso fijos
    usuario = 'e71180769r'
    contrasena = 'p5irZ9Jm4@9C#6WUaE!z9%@V'

    # Modo headless
    options = Options()
    options.headless = True
    options.add_argument("--windows-size=1920,1200")

    self.speak("Buscando la informacion...")

    # Acceso a pagina
    driver = webdriver.Chrome(options=options)
    driver.get('https://campusvirtual.uva.es/login/index.php')

    # Inicio de sesion
    driver.find_element(by=By.NAME, value='adAS_username').send_keys(usuario)
    driver.find_element(
        by=By.NAME, value='adAS_password').send_keys(contrasena)
    driver.find_element(by=By.NAME, value='adAS_submit').click()

    # Aceptar cookies
    driver.implicitly_wait(10)
    driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/div/a[1]').click()

    return driver

def numero_a_mes(x):  # Funcion que devuelve el numero de mes introducido de manera escrita
    return{
        '1': "enero",
        '2': "febrero",
        '3': "marzo",
        '4': "abril",
        '5': "mayo",
        '6': "junio",
        '7': "julio",
        '8': "agosto",
        '9': "septiembre",
        '10': "octubre",
        '11': "noviembre",
        '12': "diciembre",
    }[x]


# Funcion para dar formato a una fecha y devolverla en la respuesta
def formatear_fecha(fecha_a_formatear):
    fecha_separada = fecha_a_formatear.split(", ")
    dia_semana = fecha_separada[0]
    if (dia_semana == "Hoy"):
        hora = fecha_separada[1]
        dia = date.today().day
        mes = date.today().month
        anio = date.today().year
        fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)

    elif (dia_semana == "Mañana"):
        hora = fecha_separada[1]
        dia = date.today().day
        mes = date.today().month
        anio = date.today().year
        fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)

    else:
        hora = fecha_separada[2]
        mes_dia = fecha_separada[1].split(" ")
        dia = mes_dia[0]
        mes = mes_dia[1]
        anio = date.today().year
        fecha_formateada = str(dia) + " de " + numero_a_mes(str(mes)) + " del " + str(anio) + " a las " + str(hora)

    return fecha_formateada


class SiguienteEventoCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.evento.siguiente.intent')
    def handle_campus_evento_siguiente(self, message):
        driver = inicio_sesion(self)

        # Acceso al calendario en vista de eventos proximos
        driver.get('https://campusvirtual.uva.es/calendar/view.php?view=upcoming')

        # Obtencion de la lista de eventos proximos
        eventos_siguientes = driver.find_elements(by=By.CLASS_NAME, value='event')

        # Almacenamiento de la informacion en el fichero JSON
        fecha = str(formatear_fecha(eventos_siguientes[0].find_element(by=By.CLASS_NAME, value='col-11').text.split(" » ")[0])).split(" a las ")
        informacion['siguiente_evento'].append({
            'nombre': eventos_siguientes[0].find_element(by=By.TAG_NAME, value='h3').text,
            'fecha': fecha[0],
            'hora': fecha[1]
        })

        with open(ficheroJSON, 'w') as ficheroDatos:
                json.dump(informacion, ficheroDatos, indent=4)

        # Lectura de la informacion del fichero JSON
        with open(ficheroJSON) as ficheroEventos:
            data = json.load(ficheroEventos)
            for event in data['siguiente_evento']:
                self.speak("El " + event['fecha'] + " a las " + event['hora'] + " tienes " + event['nombre'])

        # # Respuesta con el evento proximo mas cercano
        # self.speak_dialog('campus.evento.siguiente')
        # self.speak(eventos[0].find_element(by=By.TAG_NAME, value='h3').text + formatear_fecha(
        #     eventos[0].find_element(by=By.CLASS_NAME, value='col-11').text.split(" » ")[0]))

        driver.close()


def create_skill():
    return SiguienteEventoCampus()

