from __future__ import division
__author__ = 'AnishKannan'

from django.core.management.base import BaseCommand
from siteScrape.models import SDClass, Teacher
from lxml import html, etree
import requests
import time

CAPE_PART1 = 'https://cape.ucsd.edu/responses/Results.aspx?Name='
CAPE_PART2 = '&CourseNumber='

CAPE_HEADERS = {           "Host": 'cape.ucsd.edu',
                        "Accept": ','.join([
                                    "text/html",
                                    "application/xhtml+xml",
                                    "application/xml;q=0.9,*/*;q=0.8"]),
               "Accept-Language": "en-US,en;q=0.5",
                    "User-Agent":  ' '.join([
                                    "Mozilla/5.0]",
                                    "(Macintosh; Intel Mac OS X 10_10_2)",
                                    "AppleWebKit/600.3.18",
                                    "(KHTML, like Gecko)",
                                    "Version/8.0.3 Safari/600.3.18"]),
                 "Cache-Control": "no-cache"
    }

RATE_MY_PROF_PART1 = 'http://www.ratemyprofessors.com/search.jsp?query='
RATE_MY_PROF_PART2 = '%2C+'
RATE_MY_PROF_PART3 = '+UCSD'

RATE_MY_PROF_TEACHER = 'http://www.ratemyprofessors.com'

RMP_HEADERS = {           "Host": 'ratemyprofessors.com',
                        "Accept": ','.join([
                                    "text/html",
                                    "application/xhtml+xml",
                                    "application/xml;q=0.9,*/*;q=0.8"]),
               "Accept-Language": "en-US,en;q=0.5",
                    "User-Agent":  ' '.join([
                                    "Mozilla/5.0]",
                                    "(Macintosh; Intel Mac OS X 10_10_2)",
                                    "AppleWebKit/600.3.18",
                                    "(KHTML, like Gecko)",
                                    "Version/8.0.3 Safari/600.3.18"]),
                 "Cache-Control": "no-cache"
    }

#For site verification.
certFile = 'cacert.pem'

class Command(BaseCommand):
    help = 'Scrapes sites and stores them in the database.'

    def handle(self, *args, **options):
        self.stdout.write('\n Clearing old data, please stand by')
        SDClass.objects.all().delete()

        self.stdout.write('\nScraping, please stand by')

        url = 'https://www.cse.ucsd.edu/CourseOfferings'

        r = requests.get(url)
        root = html.fromstring(r.content)

        table = root.xpath('//*[@id="node-2836"]/div[2]/table/tbody/tr')

        #Handle CSE Page row by row
        for row in table[1:]:

            #First get class data for each row.
            (title, description) = processClass(row)

            rowClass = SDClass(title = title, description = description)

            #TeacherDict stores the teachers and the flags for which quarter they are teaching.
            teacherDict = processTeacherForClass(row)

            #Storing class data in database.
            rowClass.save()

            #Situations: 1- CAPE and RMP successful. 2- CAPE successful, 3- Neither successful.
            for teacherName in teacherDict:
                #Get class data on Cape and RMP
                (fullName, responseRate, recommendRate, averageGrade, capeURL) = getCapeData(teacherName, title)

                #Cape must be successful to run RMP.
                if (responseRate != 0):
                    (RMPRating, RMPOverall, RMPUrl) = getRMPData(fullName, title)

                    #If RMP was successful
                    if (RMPRating != 0):
                        #Average between Cape and RMP
                        aggregateRating = (recommendRate + 20 * RMPRating) / 2

                    #If RMP failed
                    else:
                        aggregateRating = recommendRate
                #Both failed
                else:
                    RMPUrl = ""
                    RMPOverall = 0
                    RMPRating = 0
                    aggregateRating = 0

                print str(teacherDict[teacherName]) + " " + str(recommendRate) + " " + str(responseRate) + " " + str(averageGrade)

                print fullName + " complete!"
                rowClass.teacher_set.create(name=fullName, quarters=teacherDict[teacherName], capeRating = recommendRate, responseRate = responseRate, averageGrade = averageGrade, rateMyProfRating = RMPRating, rateMyProfRatingOverall= RMPOverall, aggregateRating = aggregateRating, CAPELink = capeURL, RMPLink=RMPUrl)

            time.sleep(10)

#Given a row, returns the title and description of a class.
def processClass(row):
    #xpath returns a list, but there will only be one match, so we get the first one and then strip /t /n out of it.
    titleSearch = row.xpath('td[1]/a/text()')
    if len(titleSearch) > 0:
        title = titleSearch[0].strip()

    #Some classes have an additional p tag to make things annoying.
    else:
        titleSearch = row.xpath('td[1]/p/a/text()')
        if len(titleSearch) > 0:
            title = titleSearch[0].strip()

        else:
            #There are no a or p tags. Just get the text there.(CSE 101X) grr
            titleSearch = row.xpath('td[1]/text()')
            if len(titleSearch) > 0:
                title = titleSearch[0].strip()

            else:
                print "Oh no"

    description = row.xpath('td[2]/text()')[0].strip()

    #Argh inconsistent html, sometimes has extra p tag. Then it has an extra "/n"
    if len(description) < 3:
        description = row.xpath('td[2]/p/text()')[0].strip()

    return (title, description)

#This method gets all teachers for a class, finds its quarters and stores them in teacherDict.
def processTeacherForClass(row):
    #Getting the teachers by quarter. 0 is fall, 1 is winter, 2 is spring.

    teacherDict = {}

    for index in range(0, 3):
        #Adding 3 to offset the first variables.
        teacherNames = row.xpath('td[' + str(index + 3) + ']/text()')[0].split('/')

        #Argh inconsistent html, sometimes has extra p tag. Then it has a "/n"
        if len(teacherNames[0]) < 2:
            teacherNames = row.xpath('td[' + str(index + 3) + ']/p/text()')[0].split('/')

        #Need to check if any of the names are repeats and also strip names
        for name in teacherNames:
            name = name.strip()
            #Some quarters have no teachers. We don't want to store that or staff.
            if name != "" and name != "Staff" and name != 'See Schedule of Classes each quarter	' and name != 'Various':
                # If name is already in the dictionary, just add the flag.
                if name in teacherDict:
                    # Fall = 4, Winter = 2, Spring = 1, need to set flags for appropriate quarters.
                    teacherDict[name] = teacherDict[name] | 2 ** (2 - index)
                # If name is new, then or with 0.
                else:
                    teacherDict[name] = 0 | 2 ** (2 - index)
    return teacherDict

#For the input teacherName and classTitle, this method returns the fullName, responseRate, recommendRate, averageGrade, and the link of the most recent class on CAPE.
def getCapeData(teacherName, classTitle):
    #Now that we've gotten names and quarters, we need to create Teacher objects and assign them to the class.
    print "trying " + teacherName

    #First, we scrape Cape data.
    capeUrl = CAPE_PART1 + teacherName + CAPE_PART2 + classTitle.replace(" ", "")

    #Get cape data for each teacher per class.
    #Cape needs headers to work.
    request = requests.get(capeUrl, verify=certFile, headers=CAPE_HEADERS)

    capeRoot = html.fromstring(request.content)
    #print(etree.tostring(row, pretty_print=True))

    #First checking if the page returned results. Then parse results.
    if (len(capeRoot.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs_ctl01_lblEmptyData"]/text()')) == 0):
        capeRow = capeRoot.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs"]/tbody/tr[1]')[0]
        #print(etree.tostring(capeRow, pretty_print=True))

        fullName = capeRow.xpath('td[1]/text()')[0].strip()
        #//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs_ctl02_lblCAPEsSubmitted"]

        #To get response rate, we divide number of students by responses.
        responseRate = round((float(capeRoot.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs_ctl02_lblCAPEsSubmitted"]/text()')[0].strip()) / float(capeRow.xpath('td[4]/text()')[0].strip())), 2)

        recommendRate = float(capeRoot.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs_ctl02_lblPercentRecommendCourse"]/text()')[0].strip().replace(' %', ''))

        averageGrade = capeRow.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs_ctl02_lblGradeExpected"]/text()')[0].strip()


    else:
        fullName = teacherName
        responseRate = 0
        recommendRate = 0
        averageGrade = "N/A"

    return (fullName, responseRate, recommendRate, averageGrade, capeUrl)

#For the input teacherName and classTitle, this method returns the average rating of the first few students on Rate my Professor and the link to the professor.
def getRMPData(teacherName, classTitle):

    #Splitting name into first, last, and middle.
    namePieces=teacherName.split(', ')

    #Making sure there is no middle name.
    namePieces[1] = namePieces[1].split(" ")[0].strip()

    #Soem teacher's names are different on RMP.
    namePieces = fixNames(teacherName, namePieces)

    RMPUrl = RATE_MY_PROF_PART1 + namePieces[0] + RATE_MY_PROF_PART2 + namePieces[1] + RATE_MY_PROF_PART3

    #Get rate my professor data for each teacher per class. Step 1: Search for professor. Step 2: Process results.
    request = requests.get(RMPUrl, verify=certFile)

    RMPRoot = html.fromstring(request.content)
    #print(etree.tostring(RMPRoot, pretty_print=True))

    #Looking for the first link to a teacher. if empty list, then no RMP reviews.
    linkSearch = RMPRoot.xpath('//*[@id="searchResultsBox"]/div[2]/ul/li/a/@href')

    #time.sleep(1)

    #First checking if the page returned results. Then parse results.
    if len(linkSearch) != 0:
        RMPTeacherURL = RATE_MY_PROF_TEACHER + linkSearch[0]

        #Now need to process specific class results.
        request = requests.get(RMPTeacherURL, verify=certFile)

        RMPRoot = html.fromstring(request.content)

        numReviews = 0
        totalSum = 0

        RMPOverall = RMPRoot.xpath('//*[@id="mainContent"]/div[2]/div[2]/div[1]/div[1]/div[1]/div/text()')[0]

        #For the reviews, classes are either "" or even.
        reviews = RMPRoot.xpath('//*[@class="" or @class="even"]')

        #Now check if that matches the specific class.
        rowNum = 0

        if len(reviews) != 0:
            for row in reviews[1:]:
                rowNum += 1

                if (row.xpath('td[2]/span[1]/span/text()')[0].strip().replace(" ", "") in classTitle.replace(" ", "")):
                    numReviews += 3
                    rating1 = row.xpath('td[1]/div[2]/div[2]/div[1]/span/text()')[0]
                    rating2 = row.xpath('td[1]/div[2]/div[2]/div[2]/span/text()')[0]
                    rating3 = row.xpath('td[1]/div[2]/div[2]/div[3]/span/text()')[0]

                    totalSum += int(rating1) + int(rating2) + int(rating3)

                    print "" + str(totalSum) + str(rating1) + str(rating2)+ str(rating3)

            #Return the average score.
            if (numReviews != 0):
                return (totalSum / numReviews, RMPOverall, RMPTeacherURL)
            #No specific reviews, just give overall score and link.
            else:
                return (0, RMPOverall, RMPTeacherURL)
    #        //*[@id="25182687"]
            #table = RMPRoot.xpath('//*[@id="mainContent"]/div[2]/div[6]/table/tbody')
            #print table
            #print(etree.tostring(table, pretty_print=True))

    return (0, 0, "")

#Yay hardcoded fixes for some names
def fixNames(teacherName, namePieces):
    #Rick Ord is listed as Rick Ord instead of Richard Ord in Rate my professor. Hardcoding a fix and hopefully other teachers don't have nicknames.
    if (teacherName == "Ord, Richard"):
        namePieces[1] = 'Rick'
    elif (teacherName == "Minnes Kemp, Mor Mia"):
        namePieces[1] = 'Mia'
    elif (teacherName == 'Altintas De Callaf, Ilkay'):
        namePieces[0] = 'Altintas'

    return namePieces