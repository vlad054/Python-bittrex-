import requests
import json
import os
import glob
#import tkinker
from enum import Enum
from tkinter import *

class TypeData(Enum):
    Markets = 1
    Summaries = 2

# class connections and requests
class Conn:
    def __init__(self):
        self.user = ''
        self.reqForMarketSummary = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market='
        self.reqForSummary = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
        self.reqForMarkets = 'https://bittrex.com/api/v1.1/public/getmarkets'
        self.prox = {'http': 'http://192.168.250.193:3128', 'https': 'https://192.168.250.193:3128'}

    def get_markets_summary(self):
        return requests.get(self.reqForSummary, proxies=self.prox).json()

    def get_markets(self):
        return requests.get(self.reqForMarkets, proxies=self.prox).json()

#class for making file and get data from btr
class Data():
    def __init__(self, param):
        self.user=''
        self.fileName = ''
        if param == 'Markets':
            self.data_for_file = 'M'
        elif param == 'Summaries':
            self.data_for_file = 'S'
        else:
            raise ValueError('Not valid param')
        self.js =''
        self.market_list = []
        self.summaries_list = []
        self.GetJSData()
        self.GetMarketList()

#return json dict
    def GetJSData(self):

        self.fileName = self.data_for_file +'dump.txt'

        if os.path.exists(self.fileName):
            with open(self.fileName) as fil:
                self.js = json.load(fil)
                fil.close()
        else:
            myCon = Conn()

            if self.data_for_file == 'M':
                self.js = myCon.get_markets()
            elif self.data_for_file == 'S':
                self.js = myCon.get_markets_summary()
            else:
                self.js={}
            fil = open(self.fileName, 'w')
            json.dump(self.js, fil, ensure_ascii=False)
            fil.close()

#        return self.js

    def GetMarketList(self):
        i = 0
        for x in self.js['result']:
            self.market_list.append(self.js['result'][i])
            #        summaries_list.append(js['result'])
            i = i + 1

    #remove files cash
    def Refresh(self):
        files = glob.glob('*dump.txt')
        for fc in files:
            os.remove(fc)
        self.js =''
        self.market_list = []

        self.GetJSData()
        self.GetMarketList()



class windowApp:

    def __init__(self, parframe,myData):
        self.parenFr = parframe
        self.idSelectedList = 0
        self.mrktDataInfo=''
        self.mdata = myData

        # list of markets
        self.marktList = Listbox(parframe, selectmode=SINGLE, bg='#FFF', fg='#099')
        self.marktList.bind('<<ListboxSelect>>', self.onSelect)
        self.marktList.pack(side=LEFT, padx=5, pady=5, fill=Y)
        self.scrollBar = Scrollbar(parframe)
        self.scrollBar.pack(side=LEFT, fill=Y)
        self.scrollBar.config(command=self.marktList.yview)

        #info frame on selected market
        self.labelTextHigh = StringVar()


        self.marktInfo = Label(parframe, width=60, textvariable=self.labelTextHigh, bg='#FFF', fg='#088', anchor='center')
        self.marktInfo.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand = True)

        #info label refresh button

        self.butRefresh = Button(parframe,text ='Refresh',command = self.Refresh)
        self.butRefresh.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

        self.fillMrktInfoData(self.mdata.market_list)

    def Refresh(self):
        self.mdata.Refresh()
        self.fillMrktInfoData(self.mdata.market_list)

    def onSelect(self, ev):
        v = ev.widget
        self.idSelectedList = int(v.curselection()[0])
        self.fillMrktInfoFrame()

    def fillMrktInfoFrame(self):
        v = 'Hight '+ str(self.mrktDataInfo[self.idSelectedList]['High']) + '\n' + '\n'\
            +'Low ' + str(self.mrktDataInfo[self.idSelectedList]['Low']) + '\n'+ '\n'\
            +'Volume ' + str(self.mrktDataInfo[self.idSelectedList]['Volume']) + '\n'+ '\n' \
            + 'Last ' + str(self.mrktDataInfo[self.idSelectedList]['Last']) + '\n' + '\n'\
            + 'BaseVolume ' + str(self.mrktDataInfo[self.idSelectedList]['BaseVolume']) + '\n' + '\n'\
            + 'TimeStamp ' + str(self.mrktDataInfo[self.idSelectedList]['TimeStamp']) + '\n' + '\n'\
            + 'Ask ' + str(self.mrktDataInfo[self.idSelectedList]['Ask']) + '\n' + '\n'\
            + 'OpenBuyOrders ' + str(self.mrktDataInfo[self.idSelectedList]['OpenBuyOrders']) + '\n' + '\n'\
            + 'OpenSellOrders ' + str(self.mrktDataInfo[self.idSelectedList]['OpenSellOrders']) + '\n' + '\n'\
            + 'PrevDay ' + str(self.mrktDataInfo[self.idSelectedList]['PrevDay']) + '\n' + '\n'\
            + 'Created ' + str(self.mrktDataInfo[self.idSelectedList]['Created'])
        self.labelTextHigh.set(v)

# get list as data
    def fillMrktInfoData(self,data):
        self.mrktDataInfo = data


    def insertInMrktList(self, ins):
        self.marktList.insert(END, ins)


if __name__ == '__main__':

    myData = Data('Markets')
#    js = myFile.GetJSData()
    print(myData.js)

    myData = Data('Summaries')
#    js = myFile.GetJSData()
    print(myData.js)

# make list of markets and summaries


    mainFrame = Tk()
    mainFrame.geometry('600x400+400+400')
    mainFrame.configure(bg='#0ff')
    mainFrame.title('Markets')

    myApp = windowApp(mainFrame,myData)

#add data to app list
    for mrkt in myData.market_list:
        myApp.insertInMrktList(mrkt['MarketName'])

#add data to app info
#    myApp.fillMrktInfoData(market_list)


    mainFrame.mainloop()






