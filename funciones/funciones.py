from asyncio.windows_events import NULL
from unittest import result
import speech_recognition as sr 
import pyttsx3, pywhatkit
from datetime import datetime
from subprocess import check_output
import random
import sqlite3 
import wikipedia
import time, os


#SPEECH_RECOGNITION (iniciador)
listener = sr.Recognizer()


engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',150)

def Hora():
    hora = datetime.now()
    if hora.strftime('%H') == '1':
        hora = hora.strftime('Es la %H y %M minutos')
    else:
        hora = hora.strftime('Son las %H y %M minutos')
    print(hora)
    engine.say(hora)
    engine.runAndWait()


def Fecha():
    dias = ["Domingo", "Lunes", "Martes","Miercoles", "Jueves", "Viernes", "Sabado"]
    meses = [None,"Enero" , "Febrero" , "Marzo" , "Abril", "Mayo", "Junio" ,"Julio" , "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre", "Diciembre"]
    date = datetime.now()
    dia = dias[int(date.strftime('%w'))]
    mes = meses[int(date.strftime('%m'))]
    fecha = date.strftime("Hoy es "+dia+' %d de '+mes)
    print(fecha)
    engine.say(fecha)
    engine.runAndWait()

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()



def CMD(comando):
    check_output(comando, shell=True)

def Abrir(aplicacion):

    if 'whatsapp' in aplicacion:
        comando = "start chrome https://web.whatsapp.com/"
        CMD(comando)
    elif 'instagram' in aplicacion:
        comando = "start chrome https://www.instagram.com/"
        CMD(comando)
    elif 'calculadora' in aplicacion:
        comando = "win32calc.exe"
        CMD(comando)
    elif 'facultad' in aplicacion:
        comando = "start chrome https://siglo21.instructure.com/"
        CMD(comando)
    elif 'youtube' in aplicacion:
        comando = "start chrome https://www.youtube.com/"
        CMD(comando)
    elif 'netflix' in aplicacion:
        comando = "start chrome https://www.netflix.com/"
        CMD(comando)
    elif 'hbo' in aplicacion:
        comando = "start chrome https://play.hbomax.com/page/urn:hbo:page:home"
        CMD(comando)
    else:
        engine.say("No se detecto la aplicacion en el sistema. ")
        engine.runAndWait()

def Confirmacion():

    respuesta = False

    afirmaciones = ['si','dale','bueno', 'esta bien', 'claro', 'bueno dale', 'claramente','positivo','afirmativo','sí']
    negaciones = ['no', 'negativo', 'na','no quiero', 'claramente no', 'esta mal','nó']

    engine.say("Confirme por favor")
    engine.runAndWait()

    while True:

        rec = escuchar()

        if type(rec) == str :

            for i in afirmaciones:
                if i in rec:
                    respuesta = True
                    engine.say("Iniciando aprendisaje")
                    engine.runAndWait()
                    return ("si")
            for i in negaciones:
                respuesta = True
                if i in rec or "cancelar" in rec:
                    engine.say("Canselando aprendisaje")
                    engine.runAndWait()
                    return ("no")

            if respuesta == False:
                engine.say("Responda con una afirmacion o una negacion, tambien puedes decir 'Cancelar'd.")


























