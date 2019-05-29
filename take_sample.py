
#Lily Steinberg

#I affirm that I have carried out the attached academic endeavors with full academic honesty,
#in accordance with the Union College Honor Code and the course syllabus.

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from StringIO import StringIO
import csv
from datetime import date, datetime

#PART 1
#creates a sample file to test code with
def take_sample (filename, sampleSize):
    i = 0
    oldFile = open(filename, 'r')
    newFile = open('newFile.txt', 'w')
    for line in oldFile:
        if i%sampleSize==0:
            newFile.write(line)
        i+=1

#PART2
# returns a dictionary that maps dates to donations for
# a given candidate from a given CSV fle
def fnd_donation_dict(candidate, filename):
    donations = []
    date = []
    neg = []

    donations, date, neg = getData(candidate, donations, date, neg, filename)

    date = sorted(date)
    plt.plot(date, donations, color = 'y')
    plt.xlabel('Date of Donation')
    plt.ylabel('Amount Donated')
    plt.title('Campaign Contributions by Date')

#PART 3
#creates a graph of donations for multiple candidates
def multiple_donations(candidate1, candidate2, filename):
    c1donations = []
    c2donations = []
    c1dates = []
    c2dates = []
    neg = []

    c1donations, c1dates, neg = getData(candidate1, c1donations, c1dates, neg, filename)

    filename.close()
    filename = open('newfile.txt', 'r')

    c2donations, c2dates, neg = getData(candidate2, c2donations, c2dates, neg, filename)

    c1dates = sorted(c1dates)
    c2dates = sorted(c2dates)

    plt.plot(c1dates,c1donations,color = 'b')
    plt.plot(c2dates,c2donations, color = 'r')
    plt.xlabel('Date of Donation')
    plt.ylabel('Amount Donated')
    plt.title('Multiple Candidates Campaign Contributions by Date')
    blue_patch = mpatches.Patch(color='blue', label=candidate1)
    red_patch = mpatches.Patch(color='red', label=candidate2)
    plt.legend(handles=[red_patch, blue_patch])

#PART 4
#creates a graph of donations for multiple candidates that cuts off at a specified date
def cumulative_graph(candidate1, candidate2, date, filename):
    c1donations = []
    c2donations = []
    c1dates = []
    c2dates = []
    neg = []

    c1donations, c1dates, neg = getData(candidate1, c1donations, c1dates, neg, filename)

    filename.close()
    filename = open('newfile.txt', 'r')

    c2donations, c2dates, neg = getData(candidate2, c2donations, c2dates, neg, filename)

    c1dates = sorted(c1dates)
    c2dates = sorted(c2dates)

    date = datetime.strptime(date, "%d-%b-%y")

    c1donations, c1dates = delete_from_list(c1donations, c1dates, date)
    c2donations, c2dates = delete_from_list(c2donations, c2dates, date)

    plt.plot(c1dates, c1donations, color='b')
    plt.plot(c2dates, c2donations, color='r')
    plt.xlabel('Date of Donation')
    plt.ylabel('Amount Donated')
    plt.title('Increased Support for Bernie')
    blue_patch = mpatches.Patch(color='blue', label=candidate1)
    red_patch = mpatches.Patch(color='red', label=candidate2)
    plt.legend(handles=[red_patch, blue_patch])

#helper method that creates new arrays without anything past the given date
def delete_from_list(donations, dates, enddate):
    i = 0
    newDates = []
    newDonations = []
    for day in dates:
        if day <= enddate:
            newDonations.append(donations[i])
            newDates.append(day)
        i+=1

    return newDonations, newDates


#PART 5
#graphs the amount of donations for each reason for a negative donation
def negative_donations(candidate, filename):
    donations = []
    date = []
    neg = []

    donations, date, neg = getData(candidate, donations, date, neg, filename)

    redesignationG = 0
    refund = 0
    reattribution = 0
    redesignationPG = 0

    redesignationG, refund, reattribution, redesignationPG = negative_reasons(neg, redesignationG, refund, reattribution, redesignationPG)

    groups = 4
    index = np.arange(groups)
    bar_width = 0.35

    y_axis = (redesignationG, refund, reattribution, redesignationPG)

    plt.bar(index, y_axis, bar_width, color = 'b')
    plt.xlabel('Reason for Negative Donation')
    plt.ylabel('Amount of Negative Donations')
    plt.xticks(index+bar_width, ('REDESIGNATION TO GENERAL', 'Refund', 'REATTRIBUTION TO SPOUSE', 'REDESIGNATION TO PRESIDENTIAL GENERAL'))
    plt.title('Negative Donations and Reasons for Ted Cruz')

#graphs only the refunds
#it is possible that these refunds were made because of insufficient funds
def refunds(candidate, filename):
    donations = []
    date = []
    neg = []

    donations, date, neg = getData(candidate, donations, date, neg, filename)

    redesignationG = 0
    refund = 0
    reattribution = 0
    redesignationPG = 0

    amountofnegs = len(neg)

    redesignation, refund, reattribution, redesignationPG = negative_reasons(neg, redesignationG, refund, reattribution, redesignationPG)

    groups = 1
    index = np.arange(groups)
    bar_width = 1

    plt.bar(index, refund, bar_width, color = 'b')
    plt.xlabel('Reason for Negative Donation')
    plt.ylabel('Amount of Negative Donations')
    plt.title('Refunds for Ted Cruz')

#helper method to get the amount of donations for each negative reason
def negative_reasons(negativearray, redesignationG, refund, reattribution, redesignationPG):
    for reason in negativearray:
        if reason == 'REDESIGNATION TO GENERAL':
            redesignationG+=1
        if reason == 'Refund':
            refund+=1
        if reason == 'REATTRIBUTION TO SPOUSE':
            reattribution+=1
        if reason == 'REDESIGNATION TO PRESIDENTIAL GENERAL':
            redesignationPG+=1

    return redesignationG, refund, reattribution, redesignationPG



#helper method to extract data from the spreadsheet
def getData(candidate, donations, date, neg, filename):
    i = 0
    for line in filename:
        if i>0:
            data = StringIO(line)
            reader = csv.reader(data, delimiter=',')

            for row in reader:
                candidateName = row[2]
                if candidateName == candidate:
                    donations.append(row[9])
                    betterDate = datetime.strptime(row[10], "%d-%b-%y")
                    date.append(betterDate)
                    if row[9].startswith('-'):
                        neg.append(row[11])

        i+=1

    return donations, date, neg

filename = open('P00000001-ALL.csv', 'r')
#filename = open('newFile.txt', 'r')
candidate1 = 'Sanders, Bernard'
candidate2 = 'Clinton, Hillary Rodham'
candidate3 = "Cruz, Rafael Edward 'Ted'"
candidate4 = "Rubio, Marco"
candidate5 = 'Bush, Jeb'
#fnd_donation_dict(candidate1, filename)
#multiple_donations(candidate1, candidate2, filename)
#cumulative_graph(candidate1, candidate2, '13-JUN-15', filename)
#negative_donations(candidate4, filename)
refunds(candidate3, filename)
plt.show()
