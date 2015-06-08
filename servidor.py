#!/usr/bin/python2
# -*- coding: utf-8 -*-

import zmq
import os
import glob
import pickle

# Directorio que vamos a compartir
directorio = raw_input("Escriba la ruta del directorio a compartir: ")


def main():

    #Se crea una instancia del contexto
    context = zmq.Context()
    #Se crea el socket con parametro peticion (REQ)
    socket = context.socket(zmq.REQ)
    #Se asocia el socket a la IP y el puerto
    socket.bind('tcp://127.0.0.1:4545')
    

    print "Directorio activo para compartir..."


    while True:
        #Usamos glob para hacer listas de archivos a partir de búsquedas con comodines en directorios
        lista = glob.glob(directorio+"/*")
        #pickle nos permite serializar la lista anterior
        ficheros = pickle.dumps(lista)
	#le pasamos al cliente la lista de ficheros que estamos compartiendo
        socket.send(ficheros)

        # Obtenemos nombre de fichero
        nomfich = socket.recv();

        # Comprobamos que el fichero existe
        if not os.path.isfile(nomfich):
            socket.send('')
            print "El archivo no se encuentra en el sistema"
            continue
        #Comvertimos el nombre del fichero en una ruta completa
        nomfich = directorio +"/"+ nomfich
	#Lo abrimos
        f = open(nomfich, 'rb')
        fichero = True
        #Y lo enviamos...
        while fichero:
            # Lee el fichero bit a bit
            fichero = f.read(128)
            if fichero:
                socket.send(fichero, zmq.SNDMORE)
            else:
                socket.send(fichero)

        #Mostramos un mensaje de finalizacion
        print "Enviado: "+nomfich


if __name__ == '__main__':
    main()
