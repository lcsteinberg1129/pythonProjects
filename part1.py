#Lily Steinberg
#I affirm that I have carried out the attached academic endeavors with full
#academic honesty, in accordance with the Union College Honor Code
#and the course syllabus.

import numpy as np
import random
import matplotlib.pyplot as plt
import sys
sys.path.append('resources/util/')
#import map_util

#this function creates a subplot with the stacked bar graph
def barGraph():

    #this creates the array for the points in the bottom bar
    bottom =  [random.randint(0, 50)]
    #this creates the array for the points in the top bar
    top = [0]
    width = 0.7

    #this calls the helper function that gives a random number between 0 and 50
    #to one variable and and gives the x coordinate to the other
    createVariables(bottom, top)

    ind = np.arange(100)
    #this says where the subplot is on the figure
    plt.subplot(321)
    #these draw the bars on the graph
    p1 = plt.bar(ind, bottom, width, color='b')
    p2 = plt.bar(ind, top, width, color='r', bottom=bottom)

#this function creates a subplot with a line graph
def lineGraph():

    #this creates the arrays to generate data with
    x1, y1, x2, y2 = [], [], [], []

    #this gets all the values for the variables
    x1, y1, x2, y2 = generateData(x1, y1, x2, y2)

    #this is where the lines get drawn on the figure
    plt.subplot(322)
    plt.plot(x1, y1, color = 'b')
    plt.plot(x2, y2, '+', color = 'r')

#this function creates a subplot with the box plots
def boxPlot():

    #these create the data for each box plot
    box1 = np.random.normal(10, 10, 50)
    box2 = np.random.normal(30, 10, 50)
    box3 = np.random.normal(50, 10, 50)

    #these draw the box plots on the figure
    plt.subplot(323)
    plt.boxplot([box1, box2, box3])

#this function creates a subplot with a scatter plot
def scatterPlot():

    #this creates the arrays to generate data with
    x1, y1, x2, y2 = [], [], [], []

    #this gets all the values for the variables
    x1, y1, x2, y2 = generateData(x1, y1, x2, y2)

    #this is where the plot is drawn on the figure
    plt.subplot(324)
    plt.scatter(x1,y1,10,color='b', alpha=.5)
    plt.scatter(x2,y2,10,color='r', marker='+', alpha=.5)

#this function creates a subplot with a map of the states
def stateMap():

    #here we open the file with the states
    file = open('resources/util/states.txt', 'r')
    #here we create the subplot to which the graph will be drawn on
    sub = plt.subplot(325)
    #this splits up the file line by line
    for line in file:
        #this calls the function in map_util that draws each state
        map_util.draw_state(sub, line)

#this function creates a subplot with a map of the counties
def countyMap():

    #here we open the file with the counties
    file = open('resources/util/counties.txt', 'r')
    #here we create the subplot to which the graph will be drawn
    sub = plt.subplot(326)
    #this splits up the file line by line
    for line in file:
        #I realized that the lines were being read in with the '/n' in the
        #string, and the draw_county function did not like that, so I had
        #to strip the line of any spaces
        fips = line.strip()
        #this calls the function in map_util that draws each county
        map_util.draw_county(sub, fips)

#this is a helper function that creates the arrays to be used for the x and y
#coordinates for the line graph and scatter plot
def generateData(x1, y1, x2, y2):
    #this creates an array for the x coordinates
    x1 = [0]
    #this creates an array for the y coordinates
    y1 = [random.randint(0,50)]
    #this calls the helper function that gives a random number between 0 and 50
    #to one variable and and gives the x coordinate to the other
    createVariables(y1, x1)

    #this creates an array of numbers from 0 to 100 to be the x coordinates
    #of the second line
    x2 = range(100)
    #this sets the y coordinate equal to the x coordinate for line 2
    y2 = x2

    return x1, y1, x2, y2

#this is a helper function that generates data that is similar for a few graphs
def createVariables(graph1, graph2):

    #this initializes the counter
    x = 1
    while (x < 100):
        #this puts a random number between 0 and 50 in the array
        graph1.append(random.randint(0,50))
        #this puts x in the array
        graph2.append(x)
        #this increases the counter
        x+=1


#here we draw all the graphs
barGraph()
lineGraph()
boxPlot()
scatterPlot()
stateMap()
countyMap()
plt.savefig('map.png')
