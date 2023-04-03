import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def convert_string(value):
    new_value = str(value)
    return new_value

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = "https://www.immoscout24.ch/en/real-estate/rent/country-switzerland-fl"
response = requests.get(url, headers=headers)
print(response)
soup = BeautifulSoup(response.content, "html.parser")
#print (soup)
#heading = soup.find_all(name='h3', class_='Box-cYFBPY hKJGPR Heading-dlrjyy bVzSiN')
#heading_data = heading.text
#print (heading)
#<h3 class="Box-cYFBPY hKJGPR Heading-daBLVV dOtgYu"
lists = soup.find_all('a',class_='Wrapper__A-kVOWTT lfjjIW')

#print (lists)
info = []

for list in lists:

    adress = list.find('span', class_='AddressLine__TextStyled-eaUAMD iBNjyG').text
    size = convert_string(list.find('h3', class_='Box-cYFBPY hKJGPR Heading-daBLVV dOtgYu')).replace('<h3 class="Box-cYFBPY hKJGPR Heading-daBLVV dOtgYu">','').replace('<!-- -->','').replace('<span>', '').replace('</span></h3>', '').replace('²','2').replace('.—','')
    #print (adress)
    #print (size)
    #print (info)
    adress.split(',')
    size.split(',')
    info.append(adress +', '+ size)

#print (info)

result = [item.split(',') for item in info]
#result2 = [item.split(',') for item in result]
print (result)


fields = ['Strasse','Ort','Kanton','Zimmer','m2','Preis']
with open('./Wohnungsdaten.csv','w', newline="\n", encoding='utf-8') as myfile:
    wr = csv.writer(myfile, delimiter = ",")
    wr.writerow(fields)
    wr.writerows(result)

#data = pd.read_csv('Wohnungsdaten.csv', sep=',')

#print(data)

#data.to_csv('Wohnungsdaten.csv',sep=',')


