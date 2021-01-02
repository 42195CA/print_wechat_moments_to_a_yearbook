#!/bin/bash
# This script is to print wechat moments to a book in the pdf format for each year
# This script should be sit in the same folder as the Moments folder you download from Wechat
# Before running this script, you should chang line 70 of print_moments_to_tex.py to your folder path 
# pre-requirement: texlive, xelatex, evince, python3 in Ubuntu (20.04 is my test version)
# input: main.tex
# python3 print_moments_to_tex.py $year to output a moments.tex
# xelatex main.tex to complie tex and output pdf
# evince is to view the pdf file
# By: Xiaoyang Liu,  xiaoyang.liu@gmail.com
# 1/2/2020

#year range 2014 to 2020, they are only two variables in this script
for year in {2014..2020}; 
do 
	echo $year;
	# remove old files
	rm -rf moments.tex main.aux main.toc main.pdf main.log main.out *~
	# prepare moments.tex for this year
	python3 print_moments_to_tex.py $year
	# prepare main.tex
	# make a backup first
	cp main.tex main.tex_back
	# shuffle a cover and logo jpg
	cp $(ls cover_*jpg  | shuf -n 1) cover.jpg
	cp $(ls logo_*jpg  | shuf -n 1) logo.jpg
	# replace year with current variable
	sed -i "s/{2000/{$year/" main.tex 
	# compile tex twice to make a correct of table of content
	xelatex main.tex 
	xelatex main.tex 
	# make a new copy of output pdf
	cp main.pdf main_$year.pdf
	#evince main.pdf & # view pdf
	rm -rf main.aux main.toc main.out main.log *~ cover.jpg logo.jpg #clean intermediate files
	# recover backup main.tex file for next usage
	mv main.tex_back main.tex
done

