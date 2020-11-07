# python 3.8

#Library
import requests as req
from bs4 import BeautifulSoup as bs
import sys
from PyQt5 import QtWidgets, uic
import json
import _thread
import time

#Global Var
global PriceSet



class Backend:
    global PriceSet
    def UrlCheck():
        global pageURL
        global PriceSet
        #Get Url
        pageURL = req.get("https://www.tgju.org/")

        #Test Url Work
        if pageURL.status_code != 200:
            return False
        elif pageURL.status_code == 200:
            return True

    def getprice():
        global pageURL
        global PriceSet
        #Change Url To Bs
        Page = bs(pageURL.text,'html.parser')
        #Get Data
        Dollar = Page.find_all("tr", {"data-market-row" : "price_dollar_rl"})
        DollarPrice = Dollar[0]['data-price']

        Eur = Page.find_all("tr", {"data-market-row" : "price_eur"})
        EurPrice = Eur[0]['data-price']

        Coin = Page.find_all("tr", {"data-market-row" : "retail_sekee"})
        CoinPrice = Coin[0]['data-price']

        CoinB = Page.find_all("tr", {"data-market-row" : "retail_sekeb"})
        CoinBPrice = CoinB[0]['data-price']    

        Gold18 = Page.find_all("tr", {"data-market-row" : "geram18"})
        Gold18Price = Gold18[0]['data-price']

        try:
            DateURL = req.get("https://www.time.ir/fa/today/")
            DateBs = bs(DateURL.text,'html.parser')
            DateBsF = DateBs.find_all("span", {"id" : "ctl00_cphMiddle_Sampa_Web_View_TimeUI_ShowDate00cphMiddle_3843_lblShamsiNumeral"})
            
            Date = DateBsF[0].text
            
            
            
        except:
            Date = "0000/00/00"
        



        #Set Data
        PriceSet = {'DollarPrice': DollarPrice , 'EurPrice': EurPrice,\
                'CoinPrice': CoinPrice, 'CoinBPrice': CoinBPrice, \
                'Gold18Price': Gold18Price, 'Date': Date}
        Backend.SaveJson()


    def LoadJson():
        global PriceSet

        try:
            with open('DataCurrencyPrice.db') as json_file:
                PriceSet = json.load(json_file)
        except:
            Backend.CreatJson()


    def SaveJson():
        global PriceSet
        with open('DataCurrencyPrice.db', 'w') as outfile:
            json.dump(PriceSet, outfile)


    def CreatJson():
        NewJson = {'DollarPrice': '0000', 'EurPrice': '0000',\
                   'CoinPrice': '0000', 'CoinBPrice': '0000', \
                   'Gold18Price': '0000', 'Date': '0000/00/00'}
        with open('DataCurrencyPrice.db', 'w') as outfile:
            json.dump(NewJson, outfile)
        Backend.LoadJson()

        


        


class Ui(QtWidgets.QMainWindow):
    global PriceSet
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('CurrencyPrice.ui', self)


        #Set Button
        self.bt = self.findChild(QtWidgets.QPushButton, 'Update') # Find the button
        self.bt.clicked.connect(lambda:self.ClickedUpdate()) # Remember to pass the definition/method, not the return value!
        
        #Set Label
        self.DollarL = self.findChild(QtWidgets.QLabel, 'DollarL')
        self.EurL = self.findChild(QtWidgets.QLabel, 'EurL')
        self.CoinL = self.findChild(QtWidgets.QLabel, 'CoinL')
        self.CoinBL = self.findChild(QtWidgets.QLabel, 'CoinBL')
        self.Gold18L = self.findChild(QtWidgets.QLabel, 'Gold18L')
        self.DateL = self.findChild(QtWidgets.QLabel, 'DateL')
        self.ErrorL = self.findChild(QtWidgets.QLabel, 'ErrorL')
        self.ErrorL.setText('')


        self.Start()


        #Set AutoUpdate Var
        self.AutoUpdateCh = self.findChild(QtWidgets.QCheckBox, 'AutoUpdate')
        self.Min = self.findChild(QtWidgets.QSpinBox, 'TimeC')

        self.AutoUpdateCh.stateChanged.connect(lambda:self.GetAuto()) # Remember to pass the definition/method, not the return value!
        #self.Min.valueChanged.connect(lambda:self.GetAuto()) # Remember to pass the definition/method, not the return value!

        
        self.show()


    def GetAuto(self):
        _thread.start_new_thread(self.Auto,())
    def Auto(self):
        while True:
            if self.AutoUpdateCh.isChecked():
                self.Min.setDisabled(True)
                self.ClickedUpdate()
                
                time.sleep(self.Min.value()*60)
                
            else:
                self.Min.setDisabled(False)
                _thread.exit_thread()


    def Start(self):
        Backend.LoadJson()
        self.SetLabel()
        self.ClickedUpdate()
        
    def DateCheck(self):
        if PriceSet['Date'] == '0000/00/00':
            self.ErrorL.setText('لطفا از اتصال به اينترنت اطمينان حاصل فرماييد')
        elif PriceSet['Date'] != '0000/00/00':
            self.ErrorL.setText('')

    def ClickedUpdate(self):
        try:
            self.ErrorL.setText('لطفا کمي منتظر بمانيد')
            if Backend.UrlCheck():
                Backend.getprice()
                self.SetLabel()
            else:
                self.ErrorL.setText('لطفا از اتصال به اينترنت اطمينان حاصل فرماييد')
        except:
            self.ErrorL.setText('لطفا از اتصال به اينترنت اطمينان حاصل فرماييد')


    def SetLabel(self):
        Backend.LoadJson()
        self.DollarL.setText(PriceSet['DollarPrice'])
        self.EurL.setText(PriceSet['EurPrice'])
        self.CoinL.setText(PriceSet['CoinPrice'])
        self.CoinBL.setText(PriceSet['CoinBPrice'])
        self.Gold18L.setText(PriceSet['Gold18Price'])
        self.DateL.setText(PriceSet['Date'])
        self.DateCheck()





app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

