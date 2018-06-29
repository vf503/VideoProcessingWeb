import re
import json
import codecs
from datetime import datetime

class JsonSuite(object):
    """description of class"""
def parse_time(time_string):

    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])

    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])

    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])

    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])



    return (hours*3600 + minutes*60 + seconds) * 1000 + milliseconds



def parse_srt(srt_string):

    srt_list = []



    for line in srt_string.split('\r\n\r\n'): #

        if line != '':

            index = int(re.match(r'\d+', line).group())



            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
       
            if line[pos:pos+1] == '\n':
                content = line[pos+1:]
            else: content = line[pos:]

            content=content.replace('\r\n','')

            start_time_string = re.findall(r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]

            end_time_string = re.findall(r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]

            start_time = parse_time(start_time_string)

            end_time = parse_time(end_time_string)

            srt_list.append( {
                'index': str(index), 
                'content': content,
                'start': str(start_time),
                'end': str(end_time),
                'PPTPagination': '0',
                'PPTOutline': '',
                'type':'SubItem',
                'IsBeginningOfParagraph':'false'
            } )

    return srt_list

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def srtToTxt(srt_string):
    srt = ''
    for line in srt_string.split('\r\n\r\n'): #
        if line != '':
            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
            if line[pos:pos+1] == '\n':
                content = line[pos+1:]
            else: content = line[pos:]
            content=content.replace('\r\n','')
            srt+=content
    return   srt




