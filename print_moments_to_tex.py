#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 12:25:51 2021
print wechat moments to a book
@author: liuxia
1/1/2021 v1
first version
1/2/2021 v2
use elephat template, use a date range variable
1/2/2021 v3
output one moments.tex for each year using the command line argument
"""
import json
import datetime
import re
import pytz
import sys

if len(sys.argv) != 2:
    print ('input year in the command line.')
    exit(1)

select_year = int(sys.argv[1])


def getChinese(context):
#    context = context.decode("utf-8") # convert context from str to unicode
    filtrate = re.compile(u'[^\u4E00-\u9FA5]') # non-Chinese unicode range
    context = filtrate.sub(r'', context) # remove all non-Chinese characters
#    context = context.encode("utf-8") # convert unicode back to str
    return context


def getLocaldatetime(tstr):
    # from str to a local time
    bjtimezone = pytz.timezone("Asia/Shanghai")
    ustimezone = pytz.timezone("America/Toronto")
    date_time_obj = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
    beijing_time = bjtimezone.localize(date_time_obj)
    usa_time = beijing_time.astimezone(ustimezone)
    return (beijing_time,usa_time)


def getCleanTexStr(line):
    #https://www.johndcook.com/blog/2019/08/31/regex-special-characters/
    special = r"\\{}$&#^_%~"
    line = re.sub(r"(?<!\\)([" + special + "])", r"\\\1", line)
#    line = line.replace('\n', '\\newline')
    return line 


def makeFig(medias):
    global outfile, fpath
    i = 0
    for media in medias:
        if media['type'] == '2':
            if i == 3 or i == 6:
                outfile.write('\\medskip\n')
                     
            img = media['content']
            outfile.write('\\begin{subfigure}{0.3\\textwidth}\n')
            outfile.write('\\centering\n')
            outfile.write('\\includegraphics[width=.8\linewidth]{'+fpath + img+'}\n')
            outfile.write('\\end{subfigure}\n')
            i = i + 1
            
            
# folder and files
fpath = '/home/liuxia/Documents/task/Moments/'
moments = fpath + 'Assets/moments.js'
comments = fpath + 'Assets/comments.js'
config = fpath + 'Assets/config.js'
photos = fpath + 'Moments/photos'
videos = fpath + 'Moments/videos'


# moments file has only 1 line, format is Callbacwhich is a Callback and json file
f = open(moments)
first = f.readline()
# extract moments data {} it is a json file
a = first.find('{')
b = first.rfind("}")+1
m = first[a:b]
mj = json.loads(m)
# extreact mements data from json data, it is array
md = mj['moments']
# for each element in the array, it is a post, could be (self-writing+photos, 1-2), (self-writing + videos 15-6) or (copy from other posts 3-2)
# this version is only to process self-writing + photos
outfile = open('moments.tex','w')
for d in md:
    if (not 'content' in d) or (not 'create_time' in d) or (not 'medias' in d) or (not 'type' in d) or (not d['type'] == '1'):
        continue
    #make date str
    date_time_str = d['create_time']
    bjtime, ustime = getLocaldatetime(date_time_str)    
    if ustime.year != select_year:
        continue
    
   # new page
    outfile.write('\\newpage\n')    
    txt = d['content']
    #make a title using the first sentence, removing non-word characters
    title = txt.split('\n')[0]
    title = title.split(' ')[0][0:10]
    title = getChinese(title)
 
       
    bjtime_str = bjtime.strftime("%Y-%m-%d")
    ustime_str = ustime.strftime("%Y-%m-%d")
    print(ustime_str)
    #make latex subsection title
    title = '\subsection{' + ustime_str + ' : ' + title + '}'    
    outfile.write(title)    
    #make a new line
    outfile.write('\n')

    #clean the body text
    txt = getCleanTexStr(txt)
    outfile.write(txt)    
    outfile.write('\n')
    
    # insert images
    medias = d['medias']
    # this version only cares of medias type = 2 images
    if type(medias) == list:
        if len(medias) > 0:
            outfile.write('\\begin{figure}[H]\n')
            makeFig(medias)
            outfile.write('\\end{figure}\n')
    

outfile.close() 
