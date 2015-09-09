__author__ = 'AnishKannan'

from django.core.management.base import BaseCommand
from siteScrape.models import SDClass, Teacher
import lxml
from lxml import html, cssselect, etree
import requests

class Command(BaseCommand):
    help = 'Scrapes sites and stores them in the database.'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping, please stand by')

        url = 'https://www.cse.ucsd.edu/CourseOfferings'

        r = requests.get(url)
        root = html.fromstring(r.content)

        #table = root.xpath('//*[@id="node-2836"]/div[2]/table/tbody/tr[2]/td[1]/a/text()')

        table = root.xpath('//*[@id="node-2836"]/div[2]/table/tbody/tr')
        #//*[@id="node-2836"]/div[2]/table/tbody/tr[2]/td[1]/a

        #print table[0].strip()

        #print (table[1].text_content())


        #Handle CSE Page row by row
        for row in table[1:]:
            #print type(root)
            #print type(table)
            print(etree.tostring(row, pretty_print=True))
            #print row.xpath('td[1]/a/text()')[0].strip()

            #print row.cssselect('td[1]')
            title = ""

            #xpath returns a list, but there will only be one match, so we get the first one and then strip /t /n out of it.
            titleSearch = row.xpath('td[1]/a/text()')
            if (len(titleSearch) > 0):
                title = titleSearch[0].strip()

            #Some classes have an additional p tag to make things annoying.
            else:
                titleSearch = row.xpath('td[1]/a/text()')
                if (len(titleSearch) > 0):
                    title = titleSearch[0].strip()

                else:
                    #There are no a or p tags. Just get the text there. ere is no /a tag (CSE 101X) grr
                    titleSearch = row.xpath('td[1]/text()')
                    if (len(titleSearch) > 0):
                        title = titleSearch[0].strip()

                    else:
                        print "Oh no"

            print title

            #newClass = SDClass()
            #print row.xpath('td[1]/a/text()')

'''        for row in root.cssselect('table[cellpadding=5] tr')[1:]:
            #data= row.cssselect('td')
            #print data[1]

            start = data[1].text_content().strip()
                 end = data[2].text_content().strip()
                 description = data[3].text_content().strip()
                 convertedStart = convertTime(start)
                 convertedEnd = convertTime(end)
                 dbStart = datetime.datetime.fromtimestamp(convertedStart)
                 dbEnd = datetime.datetime.fromtimestamp(convertedEnd)
 
                 if not Case.objects.filter(start=dbStart, end=dbEnd, court=court, description=description):
                     c = Case(start=dbStart, end=dbEnd, court=court[:60], description=description[:1024])
                     c.save()'''
