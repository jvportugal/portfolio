'''
How to run this code

1.) Install Beautiful Soup by typing '' in the command line.
2.) Install the pandas library by typing '' in the command line.
3.)
4.)
'''

from bs4 import BeautifulSoup
import pandas as pd

file=open('index.html','r')
soup=BeautifulSoup(file,'html5lib')

#Functions

def MonthToFile(text):
    text_list=text.split()
    year=str(text_list[1])
    if 'Jan' in text:
        month='01'
    if 'Feb' in text:
        month='02'
    if 'Mar' in text:
        month='03'
    if 'Apr' in text:
        month='04'
    if 'May' in text:
        month='05'
    if 'Jun' in text:
        month='06'
    if 'Jul' in text:
        month='07'
    if 'Aug' in text:
        month='08'
    if 'Sep' in text:
        month='09'
    if 'Oct' in text:
        month='10'
    if 'Nov' in text:
        month='11'
    if 'Dec' in text:
        month='12'

    return "url_"+year+month+".html"

#Code

rows=soup.find('table',{'width':600,'border':2}).find_all('tr')
headers=[]
months=[]
daily_hits=[]
daily_files=[]
daily_pages=[]
daily_visits=[]
total_sites=[]
total_kbf=[]
total_visits=[]
total_pages=[]
total_files=[]
total_hits=[]

for row in soup.find_all('td',{'nowrap':True}):
        element=row.text
        months.append(element)

for row in rows[4].find_all('th'):
    headers.append(row.text)

i=0
while(i<len(rows)-6):
    j=0
    for row in rows[i+6].find_all('td',{'align':'right'}):
        if (j==0):
            daily_hits.append(row.text)
        elif (j==1):
            daily_files.append(row.text)
        elif (j==2):
            daily_pages.append(row.text)
        elif (j==3):
            daily_visits.append(row.text)
        elif(j==4):
            total_sites.append(row.text)
        elif(j==5):
            total_kbf.append(row.text)
        elif(j==6):
            total_visits.append(row.text)
        elif(j==7):
            total_pages.append(row.text)
        elif(j==8):
            total_files.append(row.text)
        elif(j==9):
            total_hits.append(row.text)
        else:
            continue
        j=j+1 
    i=i+1

months.reverse()
daily_hits.reverse()
daily_files.reverse()
daily_pages.reverse()
daily_visits.reverse()
total_sites.reverse()
total_kbf.reverse()
total_visits.reverse()
total_pages.reverse()
total_files.reverse()
total_hits.reverse()



daily_table=pd.DataFrame(list(zip(daily_hits,daily_files,daily_pages,daily_visits)),columns=headers[0:4],index=months)
totals_table=pd.DataFrame(list(zip(total_sites,total_kbf,total_visits,total_pages,total_files,total_hits)),columns=headers[4:],index=months)

daily_table.index.name="Month"
totals_table.index.name="Month"

daily_table.to_csv('daily_averages.csv')
totals_table.to_csv('monthly_totals.csv')

month_link=soup.find_all('td',{'nowrap':True})

monthly_top_url=pd.DataFrame()

#Code Block for top_url.csv

with open('url_202303.html','r') as file:
    monthly_soup=BeautifulSoup(file,'html5lib')
    details_string=monthly_soup.find('pre').text
    details_list=details_string.splitlines()
    k=0
    for line in details_list:
        if (k>2):
            line_list=line.split()
            line_list[4:]=[' '.join(line_list[4:])]
            placeholder=pd.DataFrame({'Hits':[line_list[0]],'Hits(%)':[line_list[1]],'kBF':[line_list[2]],'kBF(%)':[line_list[3]],'URL':[line_list[4]]})
            monthly_top_url=pd.concat([monthly_top_url,placeholder],ignore_index=True)
        else:
            k=k+1
            continue

monthly_top_url.to_csv('top_url.csv')