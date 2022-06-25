from lib2to3.pgen2 import driver
import time

from mycroft import MycroftSkill, intent_file_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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


# Funcion para dar formato a una fecha y devolverla en la respuesta
def formatear_fecha(fecha_a_formatear):
    fecha_separada = fecha_a_formatear.split(", ")
    dia_semana = fecha_separada[0]
    if(dia_semana == "Mañana"):
            hora = fecha_separada[1]
            fecha_formateada = dia_semana + " a las " + hora
    else:
        hora = fecha_separada[2]
        mes_dia = fecha_separada[1].split(" ")
        dia = mes_dia[0]
        mes = mes_dia[1]
        fecha_formateada = "el " + dia_semana + " " + dia + " de " + mes + " a las " + hora
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
        eventos = driver.find_elements(by=By.CLASS_NAME, value='event')

        # Respuesta con el evento proximo mas cercano
        self.speak("Su proximo evento es " + eventos[0].find_element(by=By.TAG_NAME, value='h3').text + formatear_fecha(
            eventos[0].find_element(by=By.CLASS_NAME, value='col-11').text.split(" » ")[0]))

        driver.close()


def create_skill():
    return SiguienteEventoCampus()

