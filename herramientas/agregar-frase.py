import sqlite3
import speech_recognition as sr 
import pyttsx3

#SPEECH_RECOGNITION (iniciador)
listener = sr.Recognizer()

#PYTTSX3 (Configuracion de voz)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',150)

conexion = sqlite3.connect('DataBases/DataBases-frases.db')
cursor = conexion.cursor()
frase =""
lista=[]

def escuchar():
    rec =""

    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es-AR")
    except:
        pass
    
    rec=rec.lower()
    return (rec)

while frase!="salir":

    engine.say("Escuchando frase: ")
    engine.runAndWait()
    frase = escuchar()
    lista=[]
    lista.append(frase)
    funcion = str(input("Funcion: "))
    lista.append(funcion)
    
    if frase!="salir":
        # Insertamos un registro en la tabla de usuarios
        cursor.execute("INSERT INTO alarma VALUES(?,?)",lista)

        # Guardamos los cambios haciendo un commit
        conexion.commit()

conexion.close()