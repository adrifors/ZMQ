#!/usr/bin/python2
# -*- coding: utf-8 -*-

import zmq
import os
import pickle

def main():
  
    #Se crea una instancia del contexto
    context = zmq.Context()
    #Se crea el socket pasandole como parametro respuesta (REP)
    sock = context.socket(zmq.REP)
    #Se asocia el socket a la IP y el puerto
    sock.connect('tcp://127.0.0.1:4545')


    while True:
	#Recibimos los datos que comparte el servidor
        datos = pickle.loads(sock.recv())
        if not sock.getsockopt(zmq.RCVMORE):
            break

    print "Los ficheros disponibles son los siguientes: "

    #Mostramos los ficheros
    for elem in xrange(0,len(datos)):
        print datos[elem]

    #Pedimos el nombre del fichero que deseamos descargar
    seleccion =raw_input("Escriba el nombre del fichero que desea descargar: ")

    #Enviamos el nombre de dicho fichero
    sock.send(seleccion)
    #Abrimos el fichero, cuya ruta nos la proporciona 'os.path.basename()'
    dest = open(os.path.basename(seleccion), 'w+')

    while True:
	#Se recibe el fichero
        datos = sock.recv()
        dest.write(datos)
        if not sock.getsockopt(zmq.RCVMORE):
	    #Si no hay mas datos que enviar, entonces se para
            break
                
    dest.close()

    print "Obtenido fichero " + seleccion
    

if __name__ == '__main__':
    main()
