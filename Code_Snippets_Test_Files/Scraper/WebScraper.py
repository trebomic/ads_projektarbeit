from bs4 import BeautifulSoup
import pandas as pd
import requests
import json


class WebScraper:
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    firstJSONParameterImmo = 'listData'
    columnCaptionsImmo = ['Number of Rooms', 'Size [m²]', 'Price [CHF]', 'Street', 'Zip Code', 'City', 'Latitude', 'Longitude', 'State']
    jsonKeyValuesImmo = [['numberOfRooms'],
                         ['surfaceLiving'],
                         ['grossPrice'],
                         ['street'],
                         ['zip'],
                         ['cityName'],
                         ['latitude'],
                         ['longitude'],
                         ['state']]

    firstJSONParameterHome = 'listings'
    columnCaptionsHome = ['Number of Rooms', 'Size [m²]', 'Price [CHF]', 'Street', 'Zip Code', 'City', 'Latitude', 'Logitude']
    jsonKeyValuesHome = [['listing', 'characteristics', 'livingSpace'],
                         ['listing', 'characteristics', 'numberOfRooms'],
                         ['listing', 'prices', 'rent', 'gross'],
                         ['listing', 'address', 'street'],
                         ['listing', 'address', 'postalCode'],
                         ['listing', 'address', 'locality'],
                         ['listing', 'address', 'geoCoordinates','latitude'],
                         ['listing', 'address', 'geoCoordinates','longitude']]
    
    def extracthtmlForHomeGate(self):
        # Get the HTML Response and trim it.
        url = "https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=2"
        response = requests.get(url, headers=WebScraper.header)
        htmlResponse = BeautifulSoup(response.content, "html.parser").find_all("script")
        print(htmlResponse)

    def extractJSONForImmoScout(self, pageNumber):
        print(pageNumber)
        # Get the HTML Response and trim it. We only need the Div with id="state"
        url = "https://www.immoscout24.ch/en/real-estate/rent/country-switzerland-fl?pn=" + str(pageNumber)
        response = requests.get(url, headers=WebScraper.header)
        htmlResponse = BeautifulSoup(response.content, "html.parser").find(id="state").text

        # The needed JSON part starts with the keyValue "listData" and ends before "mapView"
        startIdx = htmlResponse.find('"listData":')
        endIdx = htmlResponse.find(',"mapView":')

        # The JSON string needs to be encased with brackets. We need to add one at the start.
        jsonString = '{' + htmlResponse[startIdx:endIdx]
        return json.loads(jsonString)

    def extractJSONForHomeGate(self, pageNumber):
        print(pageNumber)
        # Get the HTML Response and trim it.
        url = "https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=" + str(pageNumber)
        response = requests.get(url, headers=WebScraper.header)
        htmlResponse = BeautifulSoup(response.content, "html.parser").find_all("script")

        actualScript = ""
        for script in htmlResponse:
            if "window.__INITIAL_STATE__" in str(script):
                actualScript = str(script)

        startIdx = actualScript.find('"listings":')
        endIdx = actualScript.find(',"page":')
        print(actualScript[startIdx:endIdx])
        return json.loads('{' + actualScript[startIdx:endIdx] + '}')

    def createInformationMatrix(self, jsonData, firstParameter, keyValues):
        # Iterate over all available apartments and extract the following values
        infoMatrix = []
        for info in jsonData[firstParameter]:
            row = []
            for currentKey in keyValues:
                jsonTemp = info
                for key in currentKey:
                    try:
                        jsonTemp = jsonTemp[key]
                    except:
                        jsonTemp = None
                row.append(str(jsonTemp))

            infoMatrix.append(row)
        return infoMatrix

    def createPandasDataFrame(self, infoMatrix, columnCaptions):
        # Rename the column captions
        df = pd.DataFrame(infoMatrix)
        for i in range(len(columnCaptions)):
            df.rename(columns={i: columnCaptions[i]}, inplace=True)
        return df

    def runImmo(self):
        dataFrame = pd.DataFrame([])
        pageNumber = 1
        while True:
            try:
                jsonData = WebScraper.extractJSONForImmoScout(self, pageNumber)
                infoMatrix = WebScraper.createInformationMatrix(self, jsonData,
                                                                self.firstJSONParameterImmo,
                                                                self.jsonKeyValuesImmo)
                df = WebScraper.createPandasDataFrame(self, infoMatrix, self.columnCaptionsImmo)
                dataFrame = pd.concat([dataFrame, df])
                pageNumber += 1
                # if pageNumber == 10:
                #     break
            except:
                print("No more Data")
                break
        return dataFrame

    def runHome(self):
        dataFrame = pd.DataFrame([])
        pageNumber = 1
        while True:
            try:
                jsonData = WebScraper.extractJSONForHomeGate(self, pageNumber)
                infoMatrix = WebScraper.createInformationMatrix(self, jsonData,
                                                                self.firstJSONParameterHome,
                                                                self.jsonKeyValuesHome)
                df = WebScraper.createPandasDataFrame(self, infoMatrix, self.columnCaptionsHome)
                dataFrame = pd.concat([dataFrame, df])
                pageNumber += 1
                # if pageNumber == 2:
                #      break
            except:
                print("No more Data")
                break
        return dataFrame


if __name__ == '__main__':
    # WebScraper().extracthtmlForHomeGate()
    # dfImmo = WebScraper().runImmo()
    # print(dfImmo)
    dfHome = WebScraper().runHome()
    print(dfHome)

    # data = pd.concat([dfHome, dfImmo])
    # data.to_excel('Output.xlsx', index=False)