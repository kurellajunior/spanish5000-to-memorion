#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import re
import os

#row indexes
I_GERMAN = 0
I_SPANISH = 1
I_AUDIO = 2
I_PAGE_3 = 3
I_RANK = 5
I_UNIT = 6
I_TAGS = 7
I_PICTURE_GERMAN = 8
I_PICTURE_SPANISH = 9
I_PICTURE_PAGE_3 = 10
I_PICTURE_ANSWER = 11
I_WORD_TYPE = 12
I_ID = 18
I_MP3_GERMAN = 19
I_MP3_SPANISH = 20
I_MP3_PAGE_3 = 21

# Language level bits? by course
# E1-E6 -> A1, E7-E13 -> A2, E14-E21 -> B1, E22-E32 -> B2, E33-E52 -> C1
LLs = [
   2,2,2,2,2,2,
   4,4,4,4,4,4,4,
   16,16,16,16,16,16,16,16,
   32,32,32,32,32,32,32,32,32,32,32,
   128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
 ]

# defining those became necessary because the order of courses was changed but we need to keep the ids constant
sids = {
   'E01': (1,2), 'E02': (3,4), 'E03': (5,6), 'E04': (7,8), 'E05': (9,10), 'E06': (11,12), 'E07': (13,14), 'E08': (15,16), 'E09': (17,18), 'E10': (19,20), 'E11': (21,22), 'E12': (23,24),
   'E13': (103,104),
   'E14': (25,26), 'E15': (27,28), 'E16': (29,30), 'E17': (31,32), 'E18': (33,34), 'E19': (35,36), 'E20': (37,38),
   'E21': (101,102),
   'E22': (39,40), 'E23': (41,42), 'E24': (43,44), 'E25': (45,46), 'E26': (47,48), 'E27': (49,50), 'E28': (51,52), 'E29': (53,54), 'E30': (55,56), 'E31': (57,58),
   'E32': (59,60), 'E33': (61,62), 'E34': (63,64), 'E35': (65,66), 'E36': (67,68), 'E37': (69,70), 'E38': (71,72), 'E39': (73,74), 'E40': (75,76), 'E41': (77,78),
   'E42': (79,80), 'E43': (81,82), 'E44': (83,84), 'E45': (85,86), 'E46': (87,88), 'E47': (89,90), 'E48': (91,92), 'E49': (93,94), 'E50': (95,96), 'E51': (97,98),
   'E52': (99,100),
}

def replace_line_breaks(text):
   noTabs = re.compile(r'\t').sub('    ', text)
   return re.compile(r'\n').sub('<br/>', noTabs)

def build_spanish(card_definition):
   if card_definition[I_WORD_TYPE] == 'info':
      return re.compile('^', re.M).sub('</::>', card_definition[I_SPANISH])
   return card_definition[I_SPANISH]

def build_page_3(card_definition, is_mp3):
   page3 = card_definition[I_PAGE_3]
   if len(card_definition[I_AUDIO]) > 0 and not is_mp3:
      page3 += '\n[Read:"' + card_definition[I_AUDIO] + '"]'
   if len(card_definition[I_PICTURE_PAGE_3]) > 0:
      page3 += '\n' + card_definition[I_PICTURE_PAGE_3]
   page3 +=  "\n\n<b><center><font color='#808080'>" + card_definition[I_UNIT] + ", " + card_definition[I_RANK] + "</font></center></b>"
   return re.compile(r'(?<!http://)www\.').sub('http://www.',page3)

def match_type(wordType):
   return {
      'info': '[Info]',
      'nm': 'N',
      'nf': 'N',
      'nm/f': 'N',
      'v': 'V',
      'adj': 'A',
      'adv': 'A',
      'prov': 'F',
      'zahl': 'Z',
      'num': 'Z',
      'pron': 'P'
   }.get(wordType, 'X')

def build_picture(picture_name):
   return picture_name + ' w30%' if len(picture_name) > 0 else ''

def build_mp3(card_definition, is_mp3):
   if is_mp3:
      audio_files = card_definition[I_MP3_GERMAN] + '\n' if len(card_definition[I_MP3_GERMAN]) > 1  else ''
      audio_files += card_definition[I_MP3_SPANISH] + '\n' if len(card_definition[I_MP3_SPANISH]) > 1  else ''
      audio_files +=  card_definition[I_MP3_PAGE_3] if len(card_definition[I_MP3_PAGE_3]) > 1  else ' ' # non breaking space!
      return audio_files.replace(' ', '%20')
   return ''

def parse_card(card_definition, is_mp3=False):
   return (card_definition[I_ID],
      replace_line_breaks(card_definition[I_GERMAN]),
      replace_line_breaks(build_spanish(card_definition)),
      replace_line_breaks(build_page_3(card_definition, is_mp3)),
      card_definition[I_PICTURE_ANSWER],
      match_type(card_definition[I_WORD_TYPE]),
      build_picture(card_definition[I_PICTURE_GERMAN]),
      build_picture(card_definition[I_PICTURE_SPANISH]),
      replace_line_breaks(build_mp3(card_definition, is_mp3))
      )

def write_header(current_unit, csv_writer):
   course_number = int(current_unit[1:])
   order_number_german = course_number * 2 - 1
   order_number_spanish = course_number * 2
   (sid_german, sid_spanish) = sids[current_unit]
   csv_writer.writerow(("##########:next_stack",""))
   csv_writer.writerow(("#mid:hfkdkfäirt18y",""))
   csv_writer.writerow(("#sid:" + str(sid_german), "#sid:" + str(sid_spanish)))
   csv_writer.writerow(("#sn:{" + str(order_number_german).rjust(4, "0") + ">Es>De} " + current_unit, "#sn:{" + str(order_number_spanish).rjust(4, "0") + ">De>Es} " + current_unit))
   csv_writer.writerow(("#dd:35%", "#dd:45%"))
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

def read_and_split(inputFileName, tts_file_name='target/tts.tsv', mp3_file_name='target/mp3.tsv'):
   with open(inputFileName, newline='', encoding='utf8') as input_file:
      vocabulary_reader = csv.reader(input_file, delimiter=',', quotechar='"')
      with open(tts_file_name, 'w', newline='', encoding='utf8') as tts_file:
         with open(mp3_file_name, 'w', newline='', encoding='utf8') as mp3_file:
            # csv.writer(tts_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar=' ')
            tts_writer = csv.writer(tts_file, delimiter='\t', quotechar='"')
            mp3_writer = csv.writer(mp3_file, delimiter='\t', quotechar='"')
            current_unit = ""
            for row in vocabulary_reader:
               if len(row)>10 and row[I_UNIT][0] == 'E' and len(row[I_ID]) > 0:
                  if (current_unit != row[I_UNIT]):
                     current_unit = row[I_UNIT]
                     write_header(current_unit, tts_writer)
                     write_header(current_unit, mp3_writer)
                  tts_writer.writerow(parse_card(row))
                  mp3_writer.writerow(parse_card(row, True))

def main(argv):
   inputFileName = argv[0]
   if not os.path.exists('target'):
      os.makedirs('target')
   outputTTS = 'target/' + os.path.splitext(os.path.basename(inputFileName))[0] + '_tts.tsv'
   outputMP3 = 'target/' + os.path.splitext(os.path.basename(inputFileName))[0] + '_mp3.tsv'
   read_and_split(inputFileName, outputTTS, outputMP3)
   print ('TTS output file is ', outputTTS)
   print ('MP3 output file is ', outputMP3)

if __name__ == "__main__":
   main(sys.argv[1:])