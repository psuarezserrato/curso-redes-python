#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import time
import re
from pprint import pprint

maxInt = sys.maxsize
decrement = True

symbols = [
		',',';','.','!','¡','?','¿','*','&','$','%','·','<','>',':','´','/','¬','\"','\'','-','_','+','(',')','~','|','°','...','…'
	]
articles = [
		'el','la','los','las','un','una','unos','unas','y','de','ante','bajo','cabe','con','contra','de','desde','en','entre','hacia','hasta','para','por','según','segun','sin','so','sobre','tras','durante','mediante','excepto','salvo','incluso','más','mas','menos','acerca de','al lado de','alrededor de','antes de','a pesar de','cerca de','con arreglo a','con objeto de','debajo de','delante de','dentro de','después de','detrás de','encima de','en cuanto a','enfrente de','en virtud de','frente a','fuera de','lejos de','y','que', 'a','lo','le','su','se','al','#'
	]

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

words = []

file = 'credito.json'

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
        
# Esta función se encarga de limpiar los emoticones que las demas funciones no pueden quitar.
# contepla que despues de 255 en codigo ascii ya lo que sigue son simbolos raros.
def fix_emoticon(palabra):
    acumulador=''
    for letra in palabra:
        if ord(letra)<255:
            acumulador+=letra
    tmp=acumulador.strip()
    if len(tmp)>0:
        return(tmp)
    else:
        return None
        
        
def limpiaTexto(text):
	# Buscamos y quitamos las URLs de todo el texto
	# Referencia: https://docs.python.org/2/library/re.html
	text = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+','',text)

	# Buscamos y quitamos los caracteres especiales
	for s in symbols:
		cadena = s.decode('utf-8')
		text = text.lower().replace(cadena,'')

	# Buscamos y quitamos las palabras que no queremos en el texto
	for s in articles:
		cadena = ' '+s.decode('utf-8')+' '
		text = text.replace(cadena,' ')

	#Referencia: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
	text = emoji_pattern.sub(r'', text)

	return text

def creaDiccionario(text):
	# Con la funcion split tomamos un texto y pasamos cada palabra a una lista
	words_temp = text.split()

	# Para cada palabra en words_temp verificamos si existe en words global, sino esta
	# entonces lo agregamos
	for word in words_temp:
	 	if (word not in words) and (is_number(word) != True):
	 		words.append(word)

	#words = sorted(words)
	return sorted(words) 
	
# Referencia: https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

#Abrimos el archivo de tweets
with open(file, 'rb') as jsonFile:
	# Por cada tweeet
	for line in jsonFile:

		try:
			tw = json.loads(line)
			text = tw['text']

			text = limpiaTexto(text)
			text=fix_emoticon(text)
			words = creaDiccionario(text)			
			
		except Exception as e:
			print e


with open("palabras_credito.json","a") as archivo:
    archivo.write(json.dumps(words))
    archivo.write('\n')

archivo.close()

#print words
print len(words)
