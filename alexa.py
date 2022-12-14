import speech_recognition as sr 
import pyttsx3, pywhatkit
from datetime import datetime
from subprocess import check_output
import random
import sqlite3 
from funciones.funciones import *


gracias = ["No es nada, suerte...","¡No te preocupes!","Está bien", "Sin problema","No hay de qué","Es un placer", "Con mucho gusto", "Por nada, es un placer ayudar."]


#SPEECH_RECOGNITION (iniciador)
listener = sr.Recognizer()



#PYTTSX3 (Configuracion de voz)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',150)

def voz(texto):
    engine.say(texto)
    engine.runAndWait()

voz("Inicializando sistemas")

#Bienvenida



#SQLITE3 (Iniciador base de datos)
con = sqlite3.connect('DataBases/DataBases-frases.db')
cursor = con.cursor()
cursor.execute('SELECT * FROM alarma')
data_frases = cursor.fetchall()




#FUNCIONES

#FUNCION INICIADOR DE FUNCIONES
def iniciador_de_funciones(funcion, orden):

        #if funcion == "reproduciryt":
        #    pywhatkit.playonyt(music)

        if funcion == "hora":
            Hora()
        if funcion =='fecha':
            Fecha()
        if funcion == 'abrir':
            orden= orden.split()
            Abrir(orden)

            

        

    
    
#FUNCION INICIADORA DE SPEECH_RECOGNITION (Comienza a escuchar)
def escuchar():

    nombre = "nasa"
    nombre = nombre.lower()
    rec =""
    
    try:
        with sr.Microphone() as source:
            
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es-ES")
        
    except ValueError:
        #print(ValueError)
        pass
   
    
    rec=rec.lower()
    if nombre in rec:
        rec = rec.replace(nombre,"")
        print("instruccion: " + str(rec))
        return (rec)

    

#FUNCION RECONOCIMIENTO DE LA FRASE
def iniciador():

    puntajemax=0
    puntajes=[]
    orden = escuchar()

    if type(orden) == str:
        
        #preparacion de la orden para su posterior comparacion con la base de datos.
        orden = orden.lower()
        copia_orden=orden
        orden = orden.split()
        
        #obtenemos la listas de frases "aprendidas"
        global data_frases

        #crearemos un bucle que recorra "data_frases"
        for i in data_frases:

            #obtenemos individualmente cada frase
            individual_data_frase = i[0]
            funcion = i[1]

            #preparacion de la "individual_data_frase" para su posterior comparacion con orden.
            individual_data_frase = individual_data_frase.lower()
            copia_frase=individual_data_frase
            individual_data_frase = individual_data_frase.split()

            #crearemos un bucle que nos ayude a comparar cada elemento de "orden" 
            #con cada elemento de"individual_data_frase"

            puntaje_de_comparacion =  len(individual_data_frase)
            puntaje = 0

            for x in orden:
                for z in individual_data_frase:
                    if x == z:
                        puntaje += 1

            calculo=(100*puntaje)/puntaje_de_comparacion

            lista = [funcion,copia_frase,calculo]
            puntajes.append(lista)
            
            if calculo > puntajemax:
                puntajemax=calculo
                puntaje_funcion=funcion
                puntaje_frase=copia_frase


        if puntajemax > 0:

            if puntajemax < 70:

                voz(f"Disculpe! Su pedido, {copia_orden}, esta relacionado con la funcion '{puntaje_funcion}'? ")
                print(f"Disculpe! Su pedido esta relacionado con la funcion '{puntaje_funcion}'? ")

                request=Confirmacion()
                if request == "si":

                    voz(f"Le gustaria agregar la su orden, '{copia_orden}' ,a la funcion {puntaje_funcion}'? ")
                    print(f"Le gustaria agregar la su orden... '{copia_orden}' a la funcion {puntaje_funcion}'? ")

                    request2=Confirmacion()
                    if request2 == "si":
                        voz("Agregando y ejecutando nueva orden")

                        #creamos lista para insertar la nueva orden  la base de datos
                        lista=[copia_orden,puntaje_funcion]
                        # Insertamos un registro en la tabla de usuarios
                        cursor.execute("INSERT INTO alarma VALUES(?,?)",lista)
                        # Guardamos los cambios haciendo un commit
                        con.commit()
                        
                        #actualizando data memoria
                        cursor.execute('SELECT * FROM alarma')
                        data_frases = cursor.fetchall()

                        print(f"Agregando y ejecutando nueva orden")
                        iniciador_de_funciones(puntaje_funcion,copia_orden)

                elif request == "no":
                    voz("repita nuevamente su orden, por favor")
                    print("repita nuevamente su orden, por favor")

            else: 
                print("Ejecutando orden...")
                iniciador_de_funciones(puntaje_funcion,copia_orden)
        else:
            voz("No le eh entendido, repita nuevamente su orden, por favor")
            print("No le eh entendido, repita nuevamente su orden, por favor")

voz("Sistemas iniciados, a sus ordenes señor")

if __name__ == '__main__':
    while True:
        iniciador()
