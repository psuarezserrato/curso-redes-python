#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import time
import re
from pprint import pprint

fileWords = 'palabras_credito.json'
fileTweets = 'credito.json'
out = 'conteo_credito.json'
words = []
listOfTweets = []
headerCsv = ['text']



#Abrimos el archivo de palabras
with open(fileWords, 'rb') as palabras:
	# cargamos las palabras en una lista
	for words in palabras:
		words = json.loads(words)

for word in words:
    headerCsv.append(word.encode('utf-8'))

with open("matriz_inversion.csv", "a") as outfile:
	csvwriter = csv.writer(outfile)
	csvwriter.writerow(headerCsv)	


#Abrimos el archivo de tweets
with open(fileTweets, 'rb') as jsonFile:
	# Por cada tweeet
	for line in jsonFile:
		try:
			tw = json.loads(line)
			text = tw['text']
			# Creamos la estructura del json
			# Donde text es el texto del tweet
			# y Words son las palabras con el numero de veces que 
			# aparece cada palabra en el texto del tweet
			dicTweets = {
				'text':text,
				'words':{}
			}

			# Por cada palabra en la lista contamos las veces que aparece en el texto
			# Referencia: https://www.tutorialspoint.com/python/list_count.htm
			for word in words:
				dicTweets['words'][word] = text.count(word)

			#listOfTweets.append(dicTweets)
			with open(out,"a") as archivo:
			    archivo.write(json.dumps(dicTweets))
			    archivo.write('\n')

			# *******************************************************

			info = [text.encode('utf-8')]
			for word in words:
				info.append(text.count(word))
			
			with open("matriz_credito.csv", "a") as outfile:
			    csvwriter = csv.writer(outfile)
			    csvwriter.writerow(info)

		except Exception as e:
			print e
#print len(listOfTweets)