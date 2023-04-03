import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


class ImmoScoutReader:
    columnCaptions = ['Number of Rooms', 'Size [m²]', 'Price [CHF]', 'Street', 'Zip Code', 'City', 'State']
    jsonKeyValues = ['numberOfRooms', 'surfaceLiving', 'grossPrice', 'street', 'zip', 'cityName', 'state']

    def getHTMLResponse(self):
        # Get the HTML Response and trim it. We only need the Div with id="state"
        url = "https://www.immoscout24.ch/en/real-estate/rent/country-switzerland-fl"
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=header)
        return BeautifulSoup(response.content, "html.parser").find(id="state").text

    def extractJSON(self, htmlResponse):
        # The needed JSON part starts with the keyValue "listData" and ends before "mapView"
        startIdx = htmlResponse.find('"listData":')
        endIdx = htmlResponse.find(',"mapView":')

        # The JSON string needs to be encased with brackets. We need to add one at the start.
        jsonString = '{' + htmlResponse[startIdx:endIdx]
        return json.loads(jsonString)

    def createInformationMatrix(self, informations):
        # Iterate over all available apartments and extract the following values
        infoMatrix = []
        for info in informations['listData']:
            row = []
            for currentKey in ImmoScoutReader.jsonKeyValues:
                try:
                    row.append(str(info[currentKey]))
                except:
                    print('No data was found for: ' + currentKey)
                    row.append(None)
            infoMatrix.append(row)
        return infoMatrix

    def createPandasDataFrame(self, infoMatrix):
        # Rename the column captions
        df = pd.DataFrame(infoMatrix)
        for i in range(len(ImmoScoutReader.columnCaptions)):
            df.rename(columns={i: ImmoScoutReader.columnCaptions[i]}, inplace=True)
        return df

    def run(self):
        htmlResponse = ImmoScoutReader.getHTMLResponse(self)
        informations = ImmoScoutReader.extractJSON(self, htmlResponse)
        infoMatrix = ImmoScoutReader.createInformationMatrix(self, informations)
        dataFrame = ImmoScoutReader.createPandasDataFrame(self, infoMatrix)
        dataFrame.to_excel('output.xlsx', index=False)


if __name__ == '__main__':
    ImmoScoutReader().run()
