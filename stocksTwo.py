import yfinance as yf
import pandas as pd 
import datetime 
from datetime import date,timedelta
from datetime import date
import matplotlib 
from matplotlib import pyplot
import numpy as np
import sqlite3
import math
import selenium
from selenium import webdriver
import time
import requests 
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 
import queue
import threading
import customtkinter
from selenium_recaptcha_solver import RecaptchaSolver
import ffmpeg
import hashlib
sqlQueryQueue = queue.PriorityQueue() 
sqlAnswersQueue = queue.PriorityQueue()

threadlimit = threading.BoundedSemaphore(2)

yf.pdr_override() 
con = sqlite3.Connection("Stocks") 
cursor = con.cursor()
root = customtkinter.CTk() 
root.geometry("600x400") 






tradewindowroot = customtkinter.CTkToplevel() 
tradewindowroot.geometry("600x400") 

cursor.execute("CREATE TABLE IF NOT EXISTS usersTest (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,Firstname TEXT,Secondname TEXT,Password TEXT,Username Text,Funds REAL,Low REAL,Medium REAL,High REAL,LowPercentage REAL,MediumPercentage REAL,HighPERCENTAGE REAL)")
con.commit() 


cursor.execute("DROP TABLE LiveTradesTest")


cursor.execute("CREATE TABLE IF NOT EXISTS LiveTradesTest (tradeID INTEGER PRIMARY KEY AUTOINCREMENT,id INTEGER ,Stock TEXT,price REAL,quantity INTEGER,Total REAL)")
con.commit() 
cursor.execute("CREATE TABLE IF NOT EXISTS stockTest (name TEXT,risk TEXT,median REAL,upper REAL,lower REAL)")
con.commit()
empty = True

cursor.execute("DROP TABLE usersTest2")


cursor.execute("CREATE TABLE IF NOT EXISTS usersTest2 (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,Firstname TEXT,Secondname TEXT,Password TEXT,Username TEXT,Funds REAL,Low REAL,Medium REAL,High REAL,LowPercentage REAL,MediumPercentage REAL,HighPercentage REAL,Lowdefecit REAL,Mediumdefecit REAL,Highdefecit)")
con.commit()

hash = hashlib.new("SHA256") 
username = hash.update("admintest".encode()) 
usernamehashed = hash.hexdigest() 

password = hash.update("password123".encode()) 
passwordhashed = hash.hexdigest() 

cursor.execute("INSERT INTO usersTest2(email,Firstname,Secondname,Password,Username,Funds,Low,Medium,High,LowPercentage,MediumPercentage,HighPercentage,Lowdefecit,Mediumdefecit,Highdefecit) VALUES ('admin@gmail.com','admin','account',?,?,10000,2000,3000,5000,20,30,50,0,0,0)",(passwordhashed,usernamehashed,))
con.commit()







def sqlThread(connectionUsed): 
    
    retrieval = sqlQueryQueue.get()
    query = retrieval[1]
    args =  retrieval[2]
    cursorUsed = retrieval[3] 

    
    cursorUsed.execute(query,args) 
    
    results = cursorUsed.fetchall() 
    try:
         
        sqlAnswersQueue.put(results) 
        
    except: 
        sqlAnswersQueue.put(results) 
        
    connectionUsed.commit()
    





path = "C:/Users/matth/Downloads/chromedriver-win64(1)/chromedriver-win64/chromedriver.exe"
service = webdriver.chrome.service.Service(path)
options = Options() 
options.add_experimental_option("detach",True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")




searchResult = []


driver = webdriver.Chrome(service=service,options=options) 
action = ActionChains(driver)



driverRequests = queue.PriorityQueue(maxsize=1) 
driverResponses = queue.Queue(maxsize=0) 

tradeBubbles = queue.Queue()

def driverThread(): 
    
    message = driverRequests.get()
    request = message[1]
      
    
    try:
        
        
        
        
        driver.get(request["tab"]) 
    
        
        item = driver.find_elements("xpath",request["toFind"]) 
        
        
        searchResult.append("Sucess")
        driverResponses.put(item[0].text,timeout=5) 

    except: 
        
        if request["origin"] == "GUI": 

            return False 
        
        else:
        
            print("stalling")
            time.sleep(10)
            
            driver.refresh() 
            
            driverRequests.put(message)
            searchResult.append("Failed")
            driverThread()
    
        
            
            # except:
                
            #     print("Oh no something went wrong")
            #     driver.get(engine.urls[request["tab"]])

    
def moveBubbles(): 

    bubbleHolder = []
   
    print("Bubble")
    for i in range(0,4): 

        bubble = tradeBubbles.get()
        bubble.move() 

        if i != 0: 
            bubbleHolder.append(bubble) 

    bubble = tradeBubbles.get() 
    bubble.initialise() 
    bubbleHolder.append(bubble)

    for bubble in bubbleHolder: 

        tradeBubbles.put(bubble) 

          
def backThread(): 
    
    print("yes")
    engine.update(1,max=1)

def tradeThread(): 

    conTrade = sqlite3.connect("Stocks") 
    cursorTrade = conTrade.cursor()
    
    
    
    print("Trade thread active") 
    while True: 

        for stock in engine.stocksAll: 

            
            
            
            
            

            

            driverRequests.put((2,{"toFind":'//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]',"tab":engine.urls[stock]}))
            
            driverThread()
            
            retrievePriceAndCurrency = driverResponses.get()
            price = retrievePriceAndCurrency.split(' ')[0] 
            
            cursorTrade.execute("SELECT risk FROM stockTest WHERE name = ?",(stock,))
            
            result = cursorTrade.fetchall()
            
            
            
            engine.makeDecision(stock,price,result[0][0],cursorTrade,conTrade)
            time.sleep(5)



today = date.today()
end = today - timedelta(30)


def merge(leftList,rightList): 

    leftCounter = 0 
    rightCounter =0 
    tempList =[]
    while leftCounter < len(leftList) and rightCounter < len(rightList): 

        if leftList[leftCounter] < rightList[rightCounter]: 
            tempList.append(leftList[leftCounter]) 
            leftCounter = leftCounter + 1 

        else: 
            tempList.append(rightList[rightCounter]) 
            rightCounter = rightCounter + 1
    tempList = tempList + leftList[leftCounter:]
    tempList = tempList + rightList[rightCounter:]
    return tempList

def mergeSort(list): 
    if len(list) <= 1: 
        return list
    mid = int(len(list)/2) 
    left = mergeSort(list[:mid]) 
    right = mergeSort(list[mid:]) 
    return merge(left,right)
    



        





class Stock(): 

    def __init__(self,name,cursorUsed,connectionUsed):
      
      self.con = connectionUsed
      self.cursor = cursorUsed
      self._name = name 
      self.price = 0
      self._ticker = ""
      self._risk = 0 
      self._updated = 0
      self.upperquartile = 0 
      self.lowerquartile = 0
      self.mean = 0 
      self.standardDeviation = 0
      self.cycles = 0
      self.spread = 0
    
    
    
    
    

    def setRisk(self,data): 
        
        mean = sum(data) / len(data)
        
    
        xsquared = [] 
        
        for x in data: 

            xsquared.append(x*x)

        
        variance = (sum(xsquared)/ (len(data) - 1)) - (mean * mean)

        
        standard_deviation = math.sqrt(variance)

        self._risk = standard_deviation 

    
    
    
    def setSpread(self,ticker): 
        
        pt = priceTable(ticker) 
        pt.setparams(interval = "1mo",end=today,start=today-datetime.timedelta(30))
        print("Params set")
        pt.getTable() 
        
        pt.getColumnsData() 
        high = pt.high 
        low = pt.low 
        self.spread = high[0] - low[0]


    def getRisk(self): 

        sqlQueryQueue.put((1,"SELECT risk FROM stockTest WHERE name=?",(self._name,),(),self.cursor))
        sqlThread(self.con)
        results = sqlAnswersQueue.get() 
        return results[0]
        
    def getQuartiles(self): 

        
        self.cursor.execute("SELECT median,upper,lower FROM stockTest WHERE name = ?",(self._name,))
        
        
        results = self.cursor.fetchall()
        
        quartiles = {"lower":results[0][2],"median":results[0][0],"upper":results[0][1]}
        return quartiles

    def getLivePrice(self): 

        

        driverRequests.put((1,{'toFind':'//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]','tab':f"https://www.google.com/search?q={self._name}+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq={self._name}+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp"}))
        driverThread()
        retrievePriceAndCurrency = driverResponses.get()
        if retrievePriceAndCurrency is not None: 
            
            try:
                priceAndCurrency = (str(retrievePriceAndCurrency)).split(" ") 
                price = priceAndCurrency[0] 
                currency = str(priceAndCurrency[1]).split("+")[0]
                
                
                currencyType = str(priceAndCurrency[1]) 
                
                
                self.price = priceAndCurrency
                return {"price":price,"currency":currency}
                
            except: 
                time.sleep(20)
                pass
        
        
        else: 
            print("Error retrieving ")
        
    def getTicker(self): 
        
            
            
            driverRequests.put((2,{'toFind':'//*[@id="rcnt"]/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div/span','tab':f"https://www.google.com/search?q={self._name}+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq={self._name}+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp"}))
            driverThread()
            retrive = driverResponses.get()
            self._ticker = str(retrive).split(" ")[1]
        
        
    def buy(self,buyPercent,type,price,name): 

         
        
        
        sqlQueryQueue.put((2,"SELECT COUNT(*) FROM usersTest2",(),self.cursor))
        sqlThread(self.con)
        time.sleep(0.5)
        results = sqlAnswersQueue.get()
       
        row_count = results[0][0]
        
        
        for user in range(1,int(row_count)+1): 
            
            
            
            
            if type == "Medium": 


            
                sqlQueryQueue.put((2,"SELECT Medium FROM usersTest2 WHERE id = (?)",(user,),self.cursor))
            
            elif type == "Low": 

                sqlQueryQueue.put((2,"SELECT Low FROM usersTest2 WHERE id = (?)",(user,),self.cursor))
            
            else: 

                sqlQueryQueue.put((2,"SELECT High FROM usersTest2 WHERE id = (?)",(user,),self.cursor))
            sqlThread(self.con)
            
            results = sqlAnswersQueue.get()
            
           
            
            moneyAvailable = float(results[0][0]) 

            
            
            if price > moneyAvailable: 
                pass
            
            else:
                toBuy = moneyAvailable * buyPercent/100 

                
                
                num = toBuy//price

                if num > 0:
                    totalPrice = num * price 

                    
                    
                    remainingFunds = moneyAvailable - totalPrice
                    
                    sqlQueryQueue.put((2,"INSERT INTO LiveTradesTest (id,Stock,price,quantity,Total) VALUES (?,?,?,?,?)",(user,self._name,price,num,totalPrice,),self.cursor))
                    sqlThread(self.con)
                    
                    results = sqlAnswersQueue.get(block=False)
                    
                    print("Bought",type,remainingFunds)
                    
                    
                    
                    sqlQueryQueue.put((2,f"UPDATE usersTest2 SET {type} = ? WHERE id = ?",(remainingFunds,user,),self.cursor))
                    sqlThread(self.con)
                    time.sleep(0.5)
                    results = sqlAnswersQueue.get(block=False)
                
                else: 

                    pass
                

    def sell(self,type,price,name): 

        sqlQueryQueue.put((2,"SELECT id,price,quantity,Total FROM LiveTradesTest WHERE Stock = ?",(self._name,),self.cursor))
        
        sqlThread(connectionUsed=self.con)
        results = sqlAnswersQueue.get()
        
        

        for trade in results: 

           
            priceDiffPercentage = (((price * trade[2])-trade[3])/trade[3]) * 1000

            
            if priceDiffPercentage >= 100: 
                numToSell = trade[2] 
                sqlQueryQueue.put((2,"DELETE FROM LiveTradesTest WHERE id=? AND price=? AND quantity=? AND Total=?",(trade[0],trade[1],trade[2],trade[3],),self.cursor))
                
                sqlThread(self.con)
                results = sqlAnswersQueue.get(block=False)
                
                
                
                
                
                additionalMoney = price * trade[2]

            
            
            else: 
                numToSell = round((trade[2] * priceDiffPercentage)/100,0)
                newTotal = (trade[2] - numToSell) * trade[1]
                newQuantity = trade[2] - numToSell
                
                sqlQueryQueue.put((2,"UPDATE LiveTradesTest SET quantity=?,Total=? WHERE id=? AND price=? AND quantity=? AND Total=?",(newQuantity,newTotal,trade[0],trade[1],trade[2],trade[3],),self.cursor))
                sqlThread(self.con)
                results = sqlAnswersQueue.get(block=False)
                
                
                
                
                
                additionalMoney = price * numToSell

            print(type)
            
            defecitsType = {"low":"Lowdefecit","medium":"Mediumdefecit","High":"Highdefecit"}
            Typedefecits = {"Lowdefecit":"low","Mediumdefecit":"medium","Highdefecit":"High"}
            
            
            sqlQueryQueue.put((2,"SELECT Low,Medium,High,Funds,Lowdefecit,Mediumdefecit,Highdefecit,LowPercentage,MediumPercentage,HighPercentage FROM usersTest WHERE id = ?",(trade[0],),self.cursor))
            sqlThread(self.con)
            query = sqlAnswersQueue.get()
            
            defecitslist = ["Lowdefecit","Mediumdefecit","Highdefecit"]
            fundsType = {"low":query[0][0],"medium":query[0][1],"High":query[0][2]}
            newFundstype = float(fundsType[type]) + additionalMoney 
            newFundstotal = float(query[0][3]) + additionalMoney
            defecits = {"Lowdefecit":query[0][4],"Mediumdefecit":query[0][5],"Highdefecit":query[0][6]}
            

            defecitslist.remove(defecitsType[type])

            for defecit in defecitslist: 

                if defecits[defecit] < 0: 

                    defecitslist.remove(defecit)



            if len(defecitslist) == 2: 

                percentageof = newFundstotal/additionalMoney

                totaldefecit = (defecits[defecitslist[0]] + defecits[defecitslist[1]]) 

                if percentageof > totaldefecit: 

                    defecit1 = 0 
                    defecit2 = 0 
                    surplusofstocktraded = 0 

                    newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((defecits[defecitslist[0]]/100)* newFundstotal)
                    newfundsstock2 = fundsType[Typedefecits[defecitslist[1]]] + ((defecits[defecitslist[1]]/100)* newFundstotal)
                    stocktraded = fundsType[type] + (((percentageof-totaldefecit)/100) * newFundstotal)
                
                
                elif percentageof == totaldefecit: 

                    defecit1 = 0 
                    defecit2 = 0 
                    surplusofstocktraded = 0
            
                    newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((defecits[defecitslist[0]]/100)* newFundstotal)
                    newfundsstock2 = fundsType[Typedefecits[defecitslist[1]]] + ((defecits[defecitslist[1]]/100)* newFundstotal) 
                    stocktraded = fundsType[type] 

                else: 

                    halfofpercentageof = percentageof/2 

                    if halfofpercentageof > defecits[defecitslist[0]]: 

                        defecit1 = 0 
                        defecit2 = defecits[defecitslist[1]] - ((halfofpercentageof-defecits[defecitslist[1]])+ halfofpercentageof) 
                        surplusofstocktraded = defecits[defecitsType[type]] + percentageof 

                        newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((defecits[defecitslist[0]]/100)* newFundstotal)
                        newfundsstock2 = fundsType[Typedefecits[defecitslist[1]]] + ((defecits[defecitslist[1]]-defecit2/100)* newFundstotal) 
                        stocktraded = fundsType[type] 

                    elif halfofpercentageof > defecits[defecitslist[1]]: 

                        defecit1 = defecits[defecitslist[0]] - ((halfofpercentageof-defecits[defecitslist[0]])+ halfofpercentageof) 
                        defecit2 = 0
                        surplusofstocktraded = defecits[defecitsType[type]] + percentageof 

                        newfundsstock2 = fundsType[Typedefecits[defecitslist[1]]] + ((defecits[defecitslist[1]]-defecit1/100)* newFundstotal)
                        newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((defecits[defecitslist[0]] /100)* newFundstotal) 
                        stocktraded = fundsType[type]
            
                    else: 

                        defecit1 = defecits[defecitslist[0]] - halfofpercentageof 
                        defecit2 = defecits[defecitslist[1]] - halfofpercentageof 
                        surplusofstocktraded = defecits[defecitsType[type]] + percentageof 

                        newfundsstock2 = fundsType[Typedefecits[defecitslist[1]]] + ((halfofpercentageof/100)* newFundstotal)
                        newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((halfofpercentageof/100)* newFundstotal) 
                        stocktraded = fundsType[type] 

                sqlQueryQueue.put((2,"UPDATE usersTest SET ?=?,Funds=?,?=?,?=?,?=?,?=? WHERE id=?",(type,stocktraded,newFundstotal,defecitsType[type],surplusofstocktraded,defecitslist[0],defecit1,Typedefecits[defecitslist[0]],newfundsstock1,Typedefecits[defecitslist[1]],newfundsstock2,trade[0],),self.cursor))
                sqlThread(self.con)
                query = sqlAnswersQueue.get()
            elif len(defecitslist) == 1: 

                percentageof = newFundstotal/additionalMoney 
                defecitOfRiskInDefecit = defecits[defecitslist[0]] 

                

                defecit1 = defecitOfRiskInDefecit-percentageof
                surplusofstocktraded = defecits[defecitsType[type]] + percentageof

                newfundsstock1 = fundsType[Typedefecits[defecitslist[0]]] + ((defecitOfRiskInDefecit/100) * newFundstotal)
                stocktraded = fundsType[type] + (((defecitOfRiskInDefecit-percentageof)/100)* newFundstotal)
                sqlQueryQueue.put((2,"UPDATE usersTest SET ?=?,Funds=?,?=?,?=?,?=? WHERE id=?",(type,stocktraded,newFundstotal,defecitsType[type],surplusofstocktraded,defecitslist[0],defecit1,Typedefecits[defecitslist[0]],newfundsstock1,trade[0],),self.cursor))
                sqlThread(self.con)
                query = sqlAnswersQueue.get()
            
            
            else: 

                pass
            
            

class priceTable(): 

    def __init__(self,ticker): 

        self.ticker = ticker
        self.interval = "" 
        self.period = "max" 
        self.start = date(2023,8,1) 
        self.end = today
        self.table = ""
        self.high = [] 
        self.low = [] 
        self.close = [] 
        self.open = [] 
        self.dateandtime = []
        
    
    
    def getTable(self): 
        print(self.ticker)
        try:
            data = pd.DataFrame(yf.download(tickers=[self.ticker],interval=self.interval,start=self.start,end=self.end)) 
        
            self.table = data 
            print("Table is finished")
        except: 

            print(f"This failed: {self.ticker}")

    def getColumnsData(self): 

        ValuesHigh = [] 
        ValuesLow = [] 
        ValuesClose = []
        ValuesOpen = []
        dateAndTime = []
        
        columns = {"Close":{"column":3,"self":self.close,"List":ValuesClose},"High":{"column":1,"self":self.high,"List":ValuesHigh},"Low":{"column":2,"self":self.low,"List":ValuesLow},"Open":{"column":0,"self":self.open,"List":ValuesOpen}}
        
        
        for i in range(len(self.table)): 


            date = self.table.index[i] 
            
            dateAndTime.append(date)
            for key in columns: 

                data = self.table.iloc[i,columns[key]["column"]] 
                
                CorrespondingList = columns[key]["List"] 
                CorrespondingList.append(data) 

        self.close = ValuesClose 
        self.open = ValuesOpen 
        self.high = ValuesHigh 
        self.low = ValuesLow 
        self.dateandtime = dateAndTime 

    def setparams(self,**kwargs): 

        

        

        

        if "interval" in kwargs: 
            self.interval = kwargs["interval"] 
        if "period" in kwargs: 
            self.period = kwargs["period"] 
        if "start" in kwargs: 
            self.start = kwargs["start"] 
        if "end" in kwargs: 
            self.end = kwargs["end"]  

class Engine(): 

    def __init__(self,con):
        self.con = con
        self.stocksAll =  ["Apple","Microsoft","Nvidia","Amazon","Facebook","Tesla","Procter and Gamble","Google","Intel","Pepsico"]
        self.stockList = {}  
        self.urls = {
    "Apple":"https://www.google.com/search?q=apple+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=apple+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Microsoft":"https://www.google.com/search?q=Microsoft+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Microsoft+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Nvidia":"https://www.google.com/search?q=Nvidea+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Nvidia+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Amazon":"https://www.google.com/search?q=Amazon+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Amazon+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Facebook":"https://www.google.com/search?q=Facebook+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Facebook+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Tesla":"https://www.google.com/search?q=Tesla+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Tesla+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Procter and Gamble":"https://www.google.com/search?q=Procter and Gamble+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Procter and Gamble+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Google":"https://www.google.com/search?q=Google+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Google+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Intel":"https://www.google.com/search?q=Intel+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Intel+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp",
    "Pepsico":"https://www.google.com/search?q=Pepsico+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq=Pepsico+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp"
} 
        
        self.windowIDs = {} 
        self.currentloggedid = ""

    
        
    def setloggedid(self,id): 
        self.currentloggedid = id

    
    
    
    def initialiseInstances(self): 

        for stock in self.stocksAll: 

            self.stockList[stock] = Stock(stock,cursor,self.con)
        
        
        
    def checkLogin(self,username,password): 

        sqlQueryQueue.put((1,"SELECT username,password FROM "))
    
    
    def insert(self): 

        
        
        
        
        
        for stock in self.stocksAll: 

            sqlQueryQueue.put(["INSERT INTO stockTest VALUES (?,"",0,0,0)",(stock,)])
            sqlThread(self.con)
            results = sqlAnswersQueue.get()
            
            
            
    
    
    def retrieve(self): 
        for stock in self.stocksAll: 

            sqlQueryQueue.put(["SELECT median,upper,lower FROM stock WHERE name = ?",(stock,)])
            sqlThread(self.con)
            results = sqlAnswersQueue.get()
            
             
            print(f"{stock}")
            print(results)

    
    def update(self,depth,max): 

        for stock in self.stocksAll:
            
            
            
            
            
            
            
            
            #driver.get(f"https://www.google.com/search?q={stock}+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq={stock}+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp")
            stockk = Stock(stock,cursor,con)
            stockk.getTicker()
            
            lowerQuartile = [] 
            medians = [] 
            upperQuartile = []
            
            for i in range(depth): 

                 
                     
                    
                    
                    
                    table = priceTable(stockk._ticker) 

                    table.setparams(interval="1m",start=today-timedelta(max),end=today)
                    
                    table.getTable() 

                    table.getColumnsData() 


                    
                    
                    sorted = mergeSort(table.close) 
                    
                    mid = sorted[len(sorted)//2] 
                    lq = sorted[len(sorted)//4] 
                    uq = sorted[(len(sorted)//4)*3] 

                    medians.append(mid) 
                    lowerQuartile.append(lq) 
                    upperQuartile.append(uq)
                    
                    
                    
                    
                    
                    
                    
                    
                    # while len(prices) < max:
                        

                        
                        
                    #     driverRequests.put((3,{"toFind":'//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]',"tab":self.urls[stock]}))
                    #     driverThread()
                    #     retrievePriceAndCurrency = driverResponses.get()
                    #     price = retrievePriceAndCurrency.split(' ')[0]
                    #     prices.append(price)
                            
                    #     time.sleep(2)                    
                    
                        
                        
                        
                        
                        
                    
                    
                    
                    # sorted = mergeSort(prices) 
                    
                    # mid = sorted[len(sorted)//2] 
                    # lq = sorted[len(sorted)//4] 
                    # uq = sorted[(len(sorted)//4)*3] 

                    # medians.append(mid) 
                    # lowerQuartile.append(lq) 
                    # upperQuartile.append(uq)
                    
                 
           
            sqlQueryQueue.put((1,"SELECT median,upper,lower FROM stockTest WHERE name = ?",(stock,),cursor))
            sqlThread(self.con)
            
            results = sqlAnswersQueue.get()
            
            
            
                    
            lowerquartile = 0
            middle = 0
            upperquartile = 0
            for i in range(depth): 

                lowerquartile += float(lowerQuartile[i]) 
                middle += float(medians[i]) 
                upperquartile += float(upperQuartile[i]) 
                

            lowerquartile = lowerquartile/depth
            middle = middle/depth   
            upperquartile = upperquartile/depth
    
            

            sqlQueryQueue.put((1,"UPDATE stockTest SET median=?,upper=?,lower=? WHERE name = ?",(middle,upperquartile,lowerquartile,stock,),cursor))
            sqlThread(self.con)
            results = sqlAnswersQueue.get() 

            print(f"Finished {stock}  Median: {middle}")
            
    
    def initialiseTabs(self): 

        for i in range(0,10):
            
            url = self.urls[i]
            driver.execute_script(f"window.open('{url}', '_blank');")            
        print("windows open")
        
        
    def assignWindowsAndID(self):    
        for i in range(1,11): 

            windowID = driver.window_handles[i] 
            driverRequests.put((1,{"toFind":'//*[@id="rcnt"]/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div/div',"tab":windowID}))
            driverThread()
            company = driverResponses.get() 
            
            
            if company == "Alphabet Inc Class A": 

                company = "Google" 

            elif company == "PepsiCo, Inc.": 

                company = "Pepsico"
    
            elif company == "Procter & Gamble Co": 

                company = "Procter and Gamble" 

            elif company == "Intel Corporation": 

                company = "Intel" 

            elif company == "Tesla Inc": 

                company = "Tesla" 

            elif company == "Meta Platforms Inc": 

                company = "Facebook"

            elif company == "Amazon.com, Inc.": 

                company = "Amazon" 

            elif company == "NVIDIA Corp": 

                company = "Nvidia" 

            elif company == "Microsoft Corp": 

                company = "Microsoft" 

            elif company == "Apple Inc": 

                company = "Apple" 

            self.windowIDs[company] = windowID
            print(f"{company} complete")

    def switchToTab(self,tab): 

        
        driver.switch_to.window(tab)
        time.sleep(2)  
        driver.refresh()

    def makeDecision(self,stockName,livePrice,type,cursorUsed,connectionUsed): 

        today = date.today()
        stock = Stock(stockName,cursorUsed,connectionUsed) 
        quartiles = stock.getQuartiles() 
        stock.getTicker()
        stock.setSpread(stock._ticker)
        spread = stock.spread
        median = quartiles["median"] 
        lower = quartiles["lower"] 
        upper = quartiles["upper"] 
        livePrice = float(livePrice)
        priceDiff = livePrice -  float(median) 
        
        
        
        
        if priceDiff < 0: 

            

            percentageOfDiff = (priceDiff/(-1*spread))*100 

            buyPercentage = percentageOfDiff/5 

            if livePrice < lower: 

                buyPercentage += 5
            print(f"Buy:{type},{buyPercentage}")
            stock.buy(buyPercentage,type,livePrice,stockName)
            print("buy has finished")
        
        elif priceDiff > 0: 

            percentageOfDiff = (priceDiff/spread)*100 

            typeofstock = {"Low":8,"Medium":14,"High":19} 
            
            if percentageOfDiff >= typeofstock[type]: 
                print("Sell")
                stock.sell(type,livePrice,stockName) 

    def signup(name,password): 
        pass


engine = Engine(con)
engine.initialiseInstances() 
print("Engine initialised")


tt = threading.Thread(None,target=tradeThread,name="trade")
tt.start()
print("tt started")
