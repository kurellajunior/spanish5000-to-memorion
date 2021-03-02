#!/usr/bin/python3

import sys
import csv
import re
import os

#row indexes
I_FILTER=0
I_GERMAN=5
I_SPANISH=6
I_AUDIO=7
I_PAGE_3=8
I_RANK=10
I_UNIT=11
I_TAGS=12
I_PICTURE_GERMAN=13
I_PICTURE_SPANISH=14
I_PICTURE_PAGE_3=15
I_PICTURE_ANSWER=16
I_WORD_TYPE=17
I_ID=23

# Language level bits? by course
# E1-E6 -> A1, E7-E12 -> A2, E13-E19 -> B1, E20-E30 -> B2, E31-E50 -> C1, E51 -> B1, E52 -> A2
LLs = [2,2,2,2,2,2,
       4,4,4,4,4,4,
       16,16,16,16,16,16,16,
       32,32,32,32,32,32,32,32,32,32,32,
       128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
       16,4]

def buildSpanish(cardDefinition):
   if cardDefinition[I_WORD_TYPE] == 'info':
      return re.compile('^', re.M).sub('</::>', cardDefinition[I_SPANISH])
   return cardDefinition[I_SPANISH]

def buildPage3(cardDefinition):
   page3 = cardDefinition[I_PAGE_3]
   if len(cardDefinition[I_AUDIO])>0:
      page3 += '\n[Read:"' + cardDefinition[I_AUDIO] + '"]'
   if len(cardDefinition[I_PICTURE_PAGE_3]) > 0:
      page3 += '\n' + cardDefinition[I_PICTURE_PAGE_3]
   page3 +=  "\n\n<b><center><font color='#808080'>" + cardDefinition[I_UNIT] + ", " + cardDefinition[I_RANK] + "</font></center></b>"
   return re.compile(r'(?<!http://)www\.').sub('http://www.',page3)

def matchType(wordType):
   return {
      'info': '[Info]',
      'nm': 'N',
      'nf': 'N',
      'nm/f': 'N', # wohin mit dem Geschlecht?
      'v': 'V',
      'adj': 'A',
      'adv': 'A',
      'prov': 'F',
      'zahl': 'Z',
      'num': 'Z',
      'pron': 'P'
   }.get(wordType, 'X')

def buildPicture(pictureName):
   return pictureName + ' w30%' if len(pictureName) > 0 else ''

def parseCard(cardDefinition):
   return (cardDefinition[I_ID],
      cardDefinition[I_GERMAN],
      buildSpanish(cardDefinition),
      buildPage3(cardDefinition),
      cardDefinition[I_PICTURE_ANSWER],
      matchType(cardDefinition[I_WORD_TYPE]),
      buildPicture(cardDefinition[I_PICTURE_GERMAN]),
      buildPicture(cardDefinition[I_PICTURE_SPANISH])
      #mp3-Namen fehlen
      )

def write_header(current_unit, csv_writer):
   course_number = int(current_unit[1:])
   id_german = course_number * 2 - 1
   id_spanish = course_number * 2
   csv_writer.writerow(("##########:next_stack",""))
   csv_writer.writerow(("#mid:hfkdkfäirt18y",""))
   csv_writer.writerow(("#sid:" + str(id_german), "#sid:" + str(id_spanish)))
   csv_writer.writerow(("#sn:{" + str(id_german).rjust(3) + ">Es>De} " + current_unit, "#sn:{" + str(id_spanish).rjust(3) + ">De>Es} " + current_unit))
   csv_writer.writerow(("#st:Simple Language",""))
   csv_writer.writerow(("#mn:Span5k 2»1", "#mn:Span5k 1»2"))
   csv_writer.writerow(("#sf:LT",""))
   csv_writer.writerow(("#tn:Span5k",""))
   csv_writer.writerow(("#tc:Yellow", "#tc:Dk Blue",""))
   csv_writer.writerow(("#df:Span5k_Images",""))
   csv_writer.writerow(("#ob:0",""))
   csv_writer.writerow(("#is:75% of screen width",""))
   csv_writer.writerow(("#am:Only Show Answer",""))
   csv_writer.writerow(("#fcicid",""))
   csv_writer.writerow(("#ao:0",""))
   csv_writer.writerow(("#ll:" + str(LLs[course_number-1]),""))
   csv_writer.writerow(("#fn:Deutsch", "#fn:Spanisch", "#fn:Extras", "#fn:AntwortBild", "#fn:WordType", "#fn:Bild I1", "#fn:Bild I2", "#fn:MP3s"))
   csv_writer.writerow(("#la:De", "#la:Es", "#la:Es"))

def readAndSplit(inputFileName, ttsFileName='target/tts.csv'):
   with open(inputFileName, newline='') as inputFile:
      vocabularyReader = csv.reader(inputFile, delimiter=',', quotechar='"')
      with open(ttsFileName, 'w', newline='') as ttsFile:
         ttsWriter = csv.writer(ttsFile, delimiter=',', quotechar='"')
         current_unit = ""
         for row in vocabularyReader:
            if len(row)>10 and row[I_FILTER]=='A' and len(row[I_ID]) > 0:
               if (current_unit != row[I_UNIT]):
                  current_unit = row[I_UNIT]
                  write_header(current_unit, ttsWriter)
               ttsWriter.writerow(parseCard(row))

def main(argv):
   inputFileName = argv[0]
   if not os.path.exists('target'):
      os.makedirs('target')
   outputTTS = 'target/tts_' + os.path.basename(inputFileName)
   readAndSplit(inputFileName, outputTTS)
   
   print ('Output file is ', outputTTS)

if __name__ == "__main__":
   main(sys.argv[1:])