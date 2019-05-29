#Lily Steinberg

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from StringIO import StringIO
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import plotly.plotly as py
py.sign_in('steinbel', 'gy61dkbg60')
import plotly.graph_objs as go
from pylab import *
from scipy import *
import re

#Function to put artists and amount of number ones in separate arrays
def scraping ():
    file = open('artists.txt', 'r')
    soup = BeautifulSoup(file, "html.parser")
    artists = []
    numbers = []
    artist = ""
    number = ""
    for link in soup.find_all('li'):
         text = link.get_text()
         unicode_char = u'\xb0'
         if unicode_char not in text:
             artist, number = reverseString(text)
             if number.isnumeric():
                  number = int(number)
                  if number>2:
                      artists.append(artist)
                      numbers.append(number)

    makeBubbleChart(artists, numbers)

#Creates bar graph
def makeBarGraph(artists, numbers):
    figure(1, figsize=(16,9))
    artists, numbers = sort(artists, numbers)
    width = 0.5
    ind = len(numbers)
    ind = np.arange(ind)
    p1 = plt.barh(ind, numbers, width, color='b')
    plt.yticks(ind+width, (artists))
    plt.axis('tight')
    savefig('barChart.png')
    plt.show()


#makes bubble chart
def makeBubbleChart(artists, numbers):
    figure(1, figsize=(16,9))
    x = []
    n = len(artists)
    x = grabDate(artists, numbers)
    y = numbers
    color = []
    area = []
    i=0
    for num in numbers:
        color.append(num)
        area.append(num*100)
        if area[i]>600:
            text(x[i], y[i], artists[i], size=11, horizontalalignment='center')
        i+=1

    sct = scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)

    axis([1950, 2016, 0, 25])
    savefig('bubblechart.png')
    show()

#creates the pie chart
def makePieChart(artists, numbers):
    figure(1, figsize=(13,9))
    labels = artists
    percents = makePercents(numbers)
    pie(percents, labels=labels, shadow = True, startangle=90)
    savefig('piechart.png')
    show()

#makes the percentages for the pie chart
def makePercents(numbers):
    percents = []
    for number in numbers:
        number = float(number)
        length = float(len(numbers))
        frac = float(number/length)
        percents.append(frac)

    return percents

#sorts the array from smallest to largest amount of number ones
def sort(artists, numbers):
    referencedList = zip(numbers, artists)
    referencedList.sort()
    artist_sorted = [artist for number, artist in referencedList]
    numbers = sorted(numbers)
    return artist_sorted, numbers

#reverses the string, this is how I split up the amount of number ones and the artist
def reverseString(str):
    rev = str[::-1]
    newRev = rev.split("(")
    newLine = [newRev[0]] + [x for x in newRev[1:]]
    number = (newLine[0])[1:]
    number = number[::-1]
    artist = (newLine[1])[1:]
    artist = artist[::-1]
    return artist, number

#Here is where I get the years for the bubble chart
#I have it go through to each artist's wikipedia page and find the first year they were active
def grabDate(artists, numbers):
    dates=[]
    dateSoups = []
    dateSoups = goThroughWikiPages(artists,numbers)
    for dateSoup in dateSoups:
        years = dateSoup.find("table",{"class":"infobox"})
        test = years.findAll(text=re.compile('Years'), limit=1)
        next_cell = test[0].find_parent('th').find_next_sibling('td').get_text()
        date = next_cell[0:4]
        dates.append(date)
    return dates

#helper method to find all the artists' wikipedia pages
def goThroughWikiPages(artists, numbers):
    file = open('artists.txt', 'r')
    soup = BeautifulSoup(file, "html.parser")
    soups = []
    for link in soup.find_all('a'):
        text = link.get_text()
        if text in artists:
            url = "https://en.wikipedia.org"+link.get('href')
            f = urllib2.urlopen(url)
            soups.append( BeautifulSoup(f,  "html.parser"))
    return soups

#function where i make the data to pass into pie and bar charts
def debutNumberOnes():
    file = open('numberones.txt', 'r')
    soup = BeautifulSoup(file, "html.parser")

    artists = []
    amount = []
    years = []

    for line in soup.findAll('li'):
        text = line.get_text()
        delim = text.split('"')
        artist = getRidOfWeirdCharacter(delim[0])
        temp = delim[2].split(")")
        year = temp[0][len(temp[0])-4:]
        if artist not in artists:
            artists.append(artist)
            amount.append(1)
            years.append([year])

        else:
            index = artists.index(artist)
            amount[index]+=1
            years[index].append(year)

    makePieChart(artists, amount)

#helper method to get rid of the character python told me wasn't allowed
def getRidOfWeirdCharacter(string):
    return string[0:len(string)-3]

scraping()
#debutNumberOnes()
#grabDate()
#makeBubbleChart()
