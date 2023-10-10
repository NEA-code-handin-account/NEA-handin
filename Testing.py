import stocksTwo
import random
from typing import Any
import threading
from stocksTwo import Engine,Stock,priceTable,sqlThread,sqlQueryQueue,sqlAnswersQueue,cursor,con,driverRequests,driverResponses,driverThread
import selenium
from selenium import webdriver
import time
import requests 
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 
import datetime
import pytz
import sqlite3
import customtkinter
import math


import matplotlib.pyplot as plt
from functools import partial
import hashlib
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import date
customtkinter.set_appearance_mode("dark") 

customtkinter.set_default_color_theme("dark-blue") 



root = stocksTwo.root



currentLoggedInID = 0




# con = sqlite3.Connection("stocktest") 
# cursor = con.cursor()

# cursor.execute("DROP TABLE usersTest2")


# cursor.execute("CREATE TABLE IF NOT EXISTS usersTest2 (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,Firstname TEXT,Secondname TEXT,Password TEXT,Username TEXT,Funds REAL,Low REAL,Medium REAL,High REAL,LowPercentage REAL,MediumPercentage REAL,HighPERCENTAGE REAL)")
# con.commit()

# hash = hashlib.new("SHA256") 
# username = hash.update("admintest".encode()) 
# usernamehashed = hash.hexdigest() 

# password = hash.update("password123".encode()) 
# passwordhashed = hash.hexdigest() 

# cursor.execute("INSERT INTO usersTest2(email,Firstname,Secondname,Password,Username,Funds,Low,Medium,High,LowPercentage,MediumPercentage,HighPERCENTAGE) VALUES ('admin@gmail.com','admin','account',?,?,100,20,30,50,20,30,50)",(passwordhashed,usernamehashed,))
# con.commit()




lowValue = 34 
mediumValue = 33 
highValue = 33

conversionsForValues = {"low":lowValue,"medium":mediumValue,"high":highValue}
othertwo = {"low":['medium','high'],"medium":['low,high'],"high":['low','medium']}

thingsToDelete = []
signupButton = 0
backButton = 0

engine = Engine(con)

def homepage(window):

    
    window.clearMainpage()
    
    
    windowHome = Homepage(window)
    
    windowHome.initialiseButtons()
    

def stockpage(stockName,window): 

     
    window.clearMainpage() 

    windowStock = StockPage(window,stockName)
    windowStock.initialiseInformation()
    windowStock.initialiseGraph()


def alterGraph(d1,d2,interval,canvas,ticker,axis,line):


    pricetable = priceTable(ticker) 
    
    
    pricetable.setparams(interval=interval,start=d1,end=d2)
    pricetable.getTable() 
    pricetable.getColumnsData() 

    dates = pricetable.dateandtime
    x = []
    xx = []
    

    for i in range(1,len(pricetable.close)+1): 

        xx.append(i)
    NeedsDate = ["1d","5d","1wk","1mo","3mo"]
    
    for date in dates: 

        
        
        if interval in NeedsDate: 
            calender = date.date()
            
            x.append(f"{calender.day}/\n{calender.month}")
    
        else: 
            da = date.date()
            
            
            timeLong = str(date).split(" ")[1] 
            time = timeLong.split("-")[0]
            x.append(f"{time}\n({da})")


    
    
    lowPrices = pricetable.low
    highPrices = pricetable.high
    
    
    lowest = 9999999 
    highest = 0
    for price in lowPrices: 

        if price < lowest: 

            lowest = price 

    for price in highPrices: 

        if price > highest: 

            highest = price
    
    
    
    axis.lines.pop(0)
    
    plt.cla()
    
    
    axis.plot(xx,pricetable.close)
    plt.ylim((lowest-1),(highest+1))
    
    
    if len(x) < 7: 

        max = len(x) 

    else: 

        max = 7
    
    
    
    
    dividor = len(x)// 7 
    xaxis = []
    xlabels = []
    
    if dividor == 0:
        
        for i in range(len(x)): 

            xaxis.append(i) 
            xlabels.append(x[i])
    
        
        
        
        plt.xticks(ticks=xx,labels=xlabels)
    
    else:
        for i in range(0,len(x),dividor): 

            xaxis.append(i) 
            xlabels.append(x[i])
        
        
        
        
        plt.xticks(ticks=xaxis,labels=xlabels)
    
    
    
    canvas.draw()



def checkGraphSettings(startday,startmonth,startyear,endday,endmonth,endyear,interval,canvas,ticker,axis,line): 

    today = date.today()
    d1 = date(int(startyear.get()),int(startmonth.get()),int(startday.get())) 
    d2 = date(int(endyear.get()),int(endmonth.get()),int(endday.get()))
    notAllowedPast60 = ["1 minuite","5 minuites","15 minuites","30 minuites","1 hour","1.5 hours"]
    
    
    interval = interval.get()
    
    if str(d2-d1).split(" ")[0] == "0:00:00": 

        daysBetweenDates = 0 
        
    else: 

        daysBetweenDates = int(str(d2-d1).split(" ")[0])
        
    
    
    if d1 > date.today() or d2 > date.today():
        messagebox.showerror('Incorrect date',"Dates cannot be in the future!!") 

        
    
    
    elif d1 > d2: 

        messagebox.showerror('Incorrect date',"Ending date cannot be before starting date!!") 
       
    
    
    
    elif daysBetweenDates > 60 and interval in notAllowedPast60: 

        messagebox.showerror('Incorrect interval',"Interval cannot be lower than 1 day when the difference between dates is greater than 60 days!!")

        
    else: 
        
        intervalConversion = {"1 minuite":"1m","5 minuites":"5m","2 minuites":"2m","15 minuites":"15m","30 minuites":"30m","1 hour":"1h","1.5 hours":"90m","1 day":"1d","1 week":"1wk","1 month":"1mo","3 months":"3mo"}
        
        intervalNew = intervalConversion[interval]
        
        alterGraph(d1,d2,intervalNew,canvas,ticker,axis,line)


def accountpage(window): 

    window.clearMainpage() 

    windowAccount = AccountPage(window) 
    windowAccount.initialiseEntries()


def searchStocks(window,entrybox): 

    
    try:
        stock = entrybox.get() 
        print(stock)
        driverRequests.put((1,{"toFind":'//*[@id="rcnt"]/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div/span',"tab":f"https://www.google.com/search?q={stock}+stock+price&sxsrf=APwXEdfHG-MZKf9EHqLpWGrWaMnyoTRjfw%3A1686587621970&ei=5UiHZIyiOqmFhbIPv6W0gAc&ved=0ahUKEwjMqNvAlL7_AhWpQkEAHb8SDXAQ4dUDCA8&uact=5&oq={stock}+stock+price&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgoIABBHENYEELADOgcIIxCKBRAnSgQIQRgAUJMGWNwQYN4TaAFwAXgAgAGIAYgBqASSAQMyLjOYAQCgAQHAAQHIAQg&sclient=gws-wiz-serp"}))
        driverThread()
        name = driverResponses.get()
        print("DRIVER",name)
        namenonas = str(name).split(":")[1] 
        stockpage(namenonas,window)
        
     
    except:
       messagebox.showerror("Stock does not exist","The stock you have searched for does not seem to exist please try again")

def updateStocks(tosell,partialsell):

    for trade in tosell: 

        sqlQueryQueue.put((1,"DELETE FROM LiveTradesTest WHERE tradeID = ? "),(trade['tradeID'],stocksTwo.cursor))
        sqlThread(con) 
        sqlAnswersQueue.get()
    
    
    for trade in partialsell: 

        sqlQueryQueue.put((1,"UPDATE LiveTradesTest SET quantity=?,Total=? WHERE tradeID = ? "),(trade['quantity'],trade['total'],trade['tradeID'],stocksTwo.cursor))
        sqlThread(con) 
        sqlAnswersQueue.get()        


def sellTrades(trades,needselling,partialsell,neededmoney,tradesdictionary):

    tradeID = trades[0][0] 

    trade = tradesdictionary[tradeID] 

    totalvalue = trade[4] 

    if totalvalue > neededmoney: 

        percentageof = neededmoney/totalvalue 
        numbertosell = math.ceil(trade[2] * percentageof)
        
        newquantity = trade[2] - numbertosell 
        newTotal = newquantity * trade[1]
        partialsell.append({'tradeID':tradeID,'quantity':newquantity,'total':newTotal})
    
        sqlQueryQueue.put((1,"SELECT risk FROM stockTest WHERE name = ?",(trade[0],),stocksTwo.cursor))
        sqlThread(con)
        risk = sqlAnswersQueue.get()
        
        sqlQueryQueue.put((1,"SELECT ? FROM stockTest WHERE id = ?",(risk[0][0],engine.currentloggedid),stocksTwo.cursor))
        sqlThread(con)
        money = sqlAnswersQueue.get() 

        newmoney = money[0][0] + (totalvalue - neededmoney)
        
        
        
        
        updateStocks(numbertosell,partialsell)
    
        return [risk,newmoney] 
    
        
    
    elif totalvalue == neededmoney: 

        
        
        needselling.append(tradeID) 

        updateStocks(numbertosell,partialsell)
        
    else: 

        neededmoney = neededmoney - totalvalue 
        needselling.append(tradeID)
        trades.pop(0)
        sellTrades(trades,needselling,partialsell,neededmoney,tradesdictionary)

def mergesortdifference(list): 

    if len(list) > 1:
 
            
            mid = len(list)//2
            left = list[:mid]
            right = list[mid:]
            
            
            mergesortdifference(left)
            mergesortdifference(right) 

            listpointer = 0
            

            while len(left) > 0 and len(right) > 0: 
                  
                    print(listpointer)
                    
                    if left[0][1] > right[0][1]: 
                        
                        list[listpointer] = left[0]  
                        
                        left.pop(0) 
                        
                    else: 
                          
                        list[listpointer] = right[0] 

                        right.pop(0) 

                        
                    listpointer +=1
            
            while len(left) > 0: 
                  
                    list[listpointer] = left[0] 
                    listpointer += 1
                    left.pop(0) 

            while len(right) > 0: 
                  
                    list[listpointer] = right[0]
                    listpointer += 1
                    right.pop(0) 
            

def AddorWithdrawmoney(addentry,withdrawentry,totalfunds,availablefunds): 

    
    
    if addentry.get() != '': 

        availablefunds = float(availablefunds) + float(addentry.get()) 
        totalfunds = float(totalfunds) + float(addentry.get())

        sqlQueryQueue.put((1,"SELECT LowPercentage,MediumPercentage,HighPercentage FROM usersTest2 WHERE id = ?",(engine.currentloggedid,),stocksTwo.cursor))
        sqlThread(con) 
        results = sqlAnswersQueue.get()

        
        
        
        newlow = totalfunds * (results[0][0]/100)
    
        newmedium =  totalfunds * (results[0][1]/100)

        newhigh = totalfunds * (results[0][2]/100)
    

        print(f"Low: {newlow},Medium: {newmedium},High: {newhigh}")
        
        
        sqlQueryQueue.put((1,"UPDATE usersTest2 SET Low = ?,Medium=?,High=?,Funds=? WHERE id=?",(newlow,newmedium,newhigh,totalfunds,engine.currentloggedid),stocksTwo.cursor))
        sqlThread(con) 
        sqlAnswersQueue.get()
    

    print("Withdrawl:",withdrawentry.get())

    if withdrawentry.get() != '': 

        if float(withdrawentry.get()) > totalfunds: 

            messagebox.showerror(title="error",message="The amount you are trying to withdraw is greater than the funds in your account.") 

        elif float(withdrawentry.get()) <= totalfunds and float(withdrawentry.get()) > availablefunds: 

            print("MONEY MONEY MONEY")
            popupwindow = customtkinter.CTkFrame(root) 

            popupwindow.place(relx=0.3,rely=0.3)
            
            
            sqlQueryQueue.put((1,"SELECT Stock,price,quantity,tradeID,Total FROM LiveTradesTest WHERE id=?",(engine.currentloggedid,),stocksTwo.cursor))
            sqlThread(con) 
            trades = sqlAnswersQueue.get() 
            tradesdictionary = {}
            stocksOwned = []
            prices = []
            tradesDifference = []
            
            for trade in trades: 
                tradesdictionary[trade[3]] = trade
                if trade[0] in stocksOwned: 

                    pass 

                else: 

                    stocksOwned.append(trade[0])

            
            for stock in stocksOwned: 

                driverRequests.put((1,{'toFind':'//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]/span[1]/span/span[1]','tab':engine.urls[stock]}))
                driverThread() 
                price = driverResponses.get()
                print(price) 
                prices.append(price)

            moneyneeded = float(withdrawentry.get()) - availablefunds
            for trade in trades: 

                
                differenceBetweenPrices = float(prices[stocksOwned.index(trade[0])])-float(trade[0])
                tradesDifference([trade[3],differenceBetweenPrices])
                
            mergesortdifference(tradesDifference)
            sell = sellTrades(tradesDifference,[],[],moneyneeded,tradesdictionary)
            
            
            risks = ["High","Medium","Low"]

            risks.remove(sell[0]) 

            newtotal = totalfunds - withdrawentry.get()
            
            sqlQueryQueue.put((1,"UPDATE usersTest2 SET ?=?,?=0,?=0,Funds=? WHERE id=?",(sell[0],sell[1],risks[0],risks[1],newtotal,engine.currentloggedid),stocksTwo.cursor))
            sqlThread(con)
            sqlAnswersQueue.get()
                
            print("update completed for momey")

        else: 

            sqlQueryQueue.put((1,"SELECT Funds,LowPercentage,MediumPercentage,HighPercentage FROM usersTest2 WHERE id=?",(engine.currentloggedid,),stocksTwo.cursor))
            sqlThread(con)
            results = sqlAnswersQueue.get()

            newtotal = float(results[0][0]) - float(withdrawentry.get())
            newlow = newtotal * (results[0][1]/100) 
            newmedium = newtotal * (results[0][2]/100) 
            newhigh = newtotal * (results[0][3]/100) 

            sqlQueryQueue.put((1,"UPDATE usersTest2 SET Low=?,Medium=?,High=?,Funds=? WHERE id=?",(newlow,newmedium,newhigh,newtotal,engine.currentloggedid,),stocksTwo.cursor))
            sqlThread(con)
            sqlAnswersQueue.get()



def ownedstocks(window): 

    window.clearMainpage() 

    stkpage = OwnedStocksPage(window) 

    stkpage.initialiseTable()

class Window(): 

    def __init__(self):
        
        self.toolbar =  customtkinter.CTkFrame(root,width = 1535,height=795*0.1,fg_color="transparent")
        self.mainwindow = customtkinter.CTkFrame(root,width = 1535,height=795*0.9,fg_color="transparent")
        

    def initialise(self): 

        self.toolbar.place(relx=0,rely=0) 
        self.mainwindow.place(relx=0,rely=0.1)


    def placeItem(self,item,paddingx,paddingy): 

        item.place(padx=paddingx,pady=paddingy) 

    
    def Button(self,master,height,width,text,paddingx,paddingy): 

        button = customtkinter.CTkButton(master=master,height=height,width=width,text=text)
        return button
    
    def textBox(self,master,height,width,text,paddingx,paddingy): 

        textbox = customtkinter.CTkEntry(master=master,width=width,height=height,placeholder_text=text)
        return textbox 
    
    
    


    
    
    def makeToolbar(self): 

        homeSearch = customtkinter.CTkButton(self.toolbar,height=(795*0.1)*0.9,width=(1535*0.21),command=partial(homepage,self),text="Homepage") 
        myStocks = customtkinter.CTkButton(self.toolbar,height=(795*0.1)*0.9,width=(1535*0.21),text="stocks",command=partial(ownedstocks,self))
        account = customtkinter.CTkButton(self.toolbar,height=(795*0.1)*0.9,width=(1535*0.21),text="Account",command=partial(accountpage,self))
        Monatization = customtkinter.CTkButton(self.toolbar,height=(795*0.1)*0.9,width=(1535*0.21),text="Monatization",command=partial(monatization,self)) 

        homeSearch.place(relx=0.02,rely=0.05)
        myStocks.place(relx=0.27,rely=0.05)
        account.place(relx=0.52,rely=0.05) 
        Monatization.place(relx=0.77,rely=0.05) 

    def clearMainpage(self): 

        self.mainwindow.destroy() 
        self.mainwindow = customtkinter.CTkFrame(root,width = 1535,height=795*0.9,fg_color="transparent")
        self.mainwindow.place(relx=0,rely=0.1)

class OwnedStocksPage(Window):

    def __init__(self,window):
        super().__init__()
        
        self.mainwindow = window.mainwindow
        
    def initialiseTable(self): 

        
        self.mainwindow.place(relx=0,rely=0.1)
        
        
        nameleft = customtkinter.CTkLabel(self.mainwindow,text="Name")
        nameleft.place(relx=0.1,rely=0)
        
        
        priceleft = customtkinter.CTkLabel(self.mainwindow,text="Price")
        priceleft.place(relx=0.2,rely=0) 

        quantityleft = customtkinter.CTkLabel(self.mainwindow,text="Quantity")
        quantityleft.place(relx=0.3,rely=0) 

        totalleft = customtkinter.CTkLabel(self.mainwindow,text="Total")
        totalleft.place(relx=0.4,rely=0)
        
        nameright = customtkinter.CTkLabel(self.mainwindow,text="Name")
        nameright.place(relx=0.6,rely=0)
        
        
        priceright = customtkinter.CTkLabel(self.mainwindow,text="Price")
        priceright.place(relx=0.7,rely=0) 

        quantityright = customtkinter.CTkLabel(self.mainwindow,text="Quantity")
        quantityright.place(relx=0.8,rely=0) 

        totalright = customtkinter.CTkLabel(self.mainwindow,text="Total")
        totalright.place(relx=0.9,rely=0)






        
        tradeleft = customtkinter.CTkFrame(master=self.mainwindow,width=1535/2*0.9,height=(795*0.9)*0.9,bg_color='#0000FF')
        tradeleft.place(relx=0.025,rely=0.05)
        
        traderight = customtkinter.CTkFrame(master=self.mainwindow,width=1535/2*0.9,height=(795*0.9)*0.9,bg_color='#0000FF')
        traderight.place(relx=0.525,rely=0.05)
        
        
        sqlQueryQueue.put((1,"SELECT id,Stock,price,quantity,Total FROM LiveTradesTest WHERE id = ?",(engine.currentloggedid,),stocksTwo.cursor))
        sqlThread(con) 
        results = sqlAnswersQueue.get()
        print(results,len(results))
        
        if len(results) > 1:
            midpoint = len(results)//2
        
        else: 
            midpoint = len(results)
        
        
        xpos = 0.05 
        lypos=0.05
        rypos = 0.05
        for trade in results[midpoint:]: 

            totalheight = (795*0.9)*0.9 
            totalwidth = 1535/2 

            pertrade = totalheight / math.ceil(len(results)/2)

            print("per trade:",pertrade)
            
            tradeframe = customtkinter.CTkFrame(master=tradeleft,width=1535/2*0.9*0.9,height=pertrade)
            tradeframe.place(relx=xpos,rely=lypos)

            name = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[1])

            quantity = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[2]) 

            price = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[3]) 

            Total = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[4]) 

            name.place(relx=0,rely=0)
            quantity.place(relx=0.26,rely=0) 
            price.place(relx=0.52,rely=0) 
            Total.place(relx=0.78,rely=0)

            lypos += pertrade/totalheight


        for trade in results[:midpoint]: 

            if len(results[:midpoint]) < 1: 

                pass 
            
            else:
            
                totalheight = (795*0.9)*0.9 
                totalwidth = 1535/2 

                pertrade = totalheight / math.ceil(len(results)/2)

                print("per trade:",pertrade)
                
                tradeframe = customtkinter.CTkFrame(master=traderight,width=1535/2*0.9*0.9,height=pertrade)
                tradeframe.place(relx=xpos,rely=rypos)

                name = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[1])

                quantity = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[2]) 

                price = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[3]) 

                Total = customtkinter.CTkLabel(master=tradeframe,width=totalwidth*0.22,height=(pertrade)*0.9,text=trade[4]) 

                name.place(relx=0,rely=0)
                quantity.place(relx=0.26,rely=0) 
                price.place(relx=0.52,rely=0) 
                Total.place(relx=0.78,rely=0)

                rypos += pertrade/totalheight

class Homepage(Window): 

    def __init__(self,window):
        super().__init__()
        self.buttons = {}
        self.mainwindow = window.mainwindow
        self.stockButtonFrame = customtkinter.CTkFrame(self.mainwindow,width=1535/2,height=795*0.9,fg_color="transparent")
    
    
    def initialiseButtons(self): 

        
        searchforstockstext = customtkinter.CTkLabel(master=self.mainwindow,text="Search for stocks",font=(customtkinter.CTkFont,90))
        searchforstockstext.place(relx=0.025,rely=0.25)

        searchbar = customtkinter.CTkEntry(master=self.mainwindow,width = 1535*0.45,height=(795*0.9)*0.2,font=(customtkinter.CTkFont,90))
        searchbar.place(relx=0.025,rely=0.4)
        self.stockButtonFrame.place(relx=0.5,rely=0)
        
        enterButton = customtkinter.CTkButton(master=self.mainwindow,text="search",width=(1535/2)*0.4,height=(795*0.9)*0.15,command=partial(searchStocks,self,searchbar))
        enterButton.place(relx=0.15,rely=0.68)
        
        width = ((81/4)/100)
        height = 921/4240
        placements = [[0.02,0.02],[0.02+width+0.05,0.02],[0.02+2*width+0.1,0.02],[0.02+3*width+0.15,0.02],[0.02,0.02+height+0.1175],[0.02+width+0.05,0.02+height+0.1175],[0.02+2*width+0.1,0.02+height+0.1175],[0.02+3*width+0.15,0.02+height+0.1175],[0.02+width+0.05,0.02+2*height+2*0.1175],[0.02+2*width+0.1,0.02+2*height+2*0.1175]]
        
        i = 0
        for stock in engine.stocksAll: 

            button = customtkinter.CTkButton(master=self.stockButtonFrame,height=24867/160,width=155.41875,text=stock,command=partial(stockpage,stock,self)) 
            
            
            button.place(relx = placements[i][0],rely = placements[i][1]) 
            i += 1 

    
class StockPage(Window): 

    def __init__(self,window,stock):
        super().__init__()
        
        self.mainwindow = window.mainwindow
        self.graphContainer = customtkinter.CTkFrame(self.mainwindow,width=(1535*0.58),height=(795*0.9)*0.95,fg_color="transparent")
        self.stock = Stock(stock,cursor,con)
    def initialiseGraph(self):
        self.graphContainer.place(relx=0.0,rely=0.05) 
        self.stock.getTicker()
        
        x = [1,2,3] 
        y = [1,2,3]
        
        
        figure, ax = plt.subplots()
        figure.set_facecolor("black")
        ax.tick_params(colors='white', which='both')
        line = ax.plot(x, y)
        figure.set_figwidth(8) 
        figure.set_figheight(8)
        
        
        startLabel = customtkinter.CTkLabel(self.graphContainer,font=("Helvetica",28),text="Start date")
        startLabel.place(relx=0.8,rely=0.15)
        
        endLabel = customtkinter.CTkLabel(self.graphContainer,font=("Helvetica",28),text="End date")
        endLabel.place(relx=0.8,rely=0.35)
        
        
        
        valuesDay = []
        valuesMonth = [] 
        valuesYear = []
        
        canvas = FigureCanvasTkAgg(figure,master=self.graphContainer) 
        canvas.get_tk_widget().place(relx=0.0,rely=0.0)




        for i in range(1,32): 

            valuesDay.append(str(i))
        
        
        for i in range(1,13): 

            valuesMonth.append(str(i)) 

        for i in range(2023,1900,-1): 

            valuesYear.append(str(i))
        
        
        startDay = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesDay)
        startDay.place(relx=0.75,rely=0.25)

        startMonth = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesMonth)
        startMonth.place(relx=0.82,rely=0.25)
        
        startYear = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesYear)
        startYear.place(relx=0.89,rely=0.25)
        

        endDay = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesDay)
        endDay.place(relx=0.75,rely=0.45)

        endMonth = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesMonth)
        endMonth.place(relx=0.82,rely=0.45)
        
        endYear = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=valuesYear)
        endYear.place(relx=0.89,rely=0.45) 

        intervalLabel = customtkinter.CTkLabel(self.graphContainer,font=("Helvetica",28),text="Interval") 
        interval = customtkinter.CTkOptionMenu(master=self.graphContainer,width=((1535*0.58)*0.01),height=((795*0.9)*0.05),values=["1 minuite","5 minuites","15 minuites","30 minuites","1 hour","1.5 hours","1 day","1 week","1 month","3 months"])
        intervalLabel.place(relx=0.8,rely=0.55) 
        interval.place(relx=0.82,rely=0.65)

        
        interval.set("1 day")
        
        endDay.set(date.today().day) 
        endMonth.set(date.today().month) 
        endYear.set(date.today().year)

        
        if int(date.today().month) == 1: 

        
            startDay.set(date.today().day) 
            startMonth.set(12)
            startYear.set(date.today().year-1)

        else: 
            startDay.set(date.today().day) 
            startMonth.set(date.today().month - 1)
            startYear.set(date.today().year)
        
        

        self.stock.getTicker()
        
        checkGraphSettings(startDay,startMonth,startYear,endDay,endMonth,endYear,interval,canvas,self.stock._ticker,ax,line)
        deployChangesButton = customtkinter.CTkButton(master=self.graphContainer,width= ((1535*0.58)*0.2),height=((795*0.9)*0.1),text="Deploy changes",command= partial(checkGraphSettings,startDay,startMonth,startYear,endDay,endMonth,endYear,interval,canvas,self.stock._ticker,ax,line))
        deployChangesButton.place(relx=0.75,rely=0.75)
    
    def initialiseInformation(self):
        
        stockLabel = customtkinter.CTkLabel(master=self.mainwindow,font=("Helvetica",60),text=self.stock._name) 
        stockLabel.place(relx=0.02,rely=0.02)

        
        
        
        result = self.stock.getLivePrice()
        
        priceWCurrency = f"{result['price']} {result['currency']}"
        priceLabel = customtkinter.CTkLabel(master=self.mainwindow,font=("Helvetica",100),text=priceWCurrency,fg_color='transparent') 
        priceLabel.place(relx=0.6,rely=0.05) 

        
class AccountPage(Window): 

    def __init__(self,window):
        super().__init__() 
        self.mainwindow = window.mainwindow 

    def initialiseEntries(self): 

        global lowSliderr 
        global mediumSliderr 
        global HighSliderr
        
        
        
        sqlQueryQueue.put((1,"SELECT LowPercentage,MediumPercentage,HighPercentage FROM usersTest2 WHERE id = ?",(engine.currentloggedid,),cursor))
        sqlThread(con) 
        results = sqlAnswersQueue.get()
        
        firstnamelabel = customtkinter.CTkLabel(self.mainwindow,text="Firstname:",text_color="#FFFFFF",width=(1535*0.5)*0.19,font=(customtkinter.CTkFont,60)) 

        firstnameentry = customtkinter.CTkEntry(self.mainwindow,fg_color="transparent",width=(1535*0.5)*0.19,height=(795*0.9)*0.1) 

        firstnamelabel.place(relx=0.05,rely=0.05) 
        firstnameentry.place(relx=0.30,rely=0.05)

        secondnamelabel = customtkinter.CTkLabel(self.mainwindow,text="Secondname:",text_color="#FFFFFF",width=(1535*0.5)*0.19,height=(795*0.9)*0.1,font=(customtkinter.CTkFont,60)) 

        secondnameentry = customtkinter.CTkEntry(self.mainwindow,fg_color="transparent",width=(1535*0.5)*0.19,height=(795*0.9)*0.1) 

        secondnamelabel.place(relx=0.05,rely=0.25) 
        secondnameentry.place(relx=0.30,rely=0.25) 

        usernamelabel = customtkinter.CTkLabel(self.mainwindow,text="Username:",text_color="#FFFFFF",width=(1535*0.5)*0.19,height=(795*0.9)*0.1,font=(customtkinter.CTkFont,60)) 

        usernameentry = customtkinter.CTkEntry(self.mainwindow,fg_color="transparent",width=(1535*0.5)*0.19,height=(795*0.9)*0.1) 

        usernamelabel.place(relx=0.05,rely=0.45) 
        usernameentry.place(relx=0.30,rely=0.45) 

        passwordlabel = customtkinter.CTkLabel(self.mainwindow,text="Password:",text_color="#FFFFFF",width=(1535*0.5)*0.19,height=(795*0.9)*0.1,font=(customtkinter.CTkFont,60)) 

        passwordentry = customtkinter.CTkEntry(self.mainwindow,fg_color="transparent",width=(1535*0.5)*0.19,height=(795*0.9)*0.1) 

        passwordlabel.place(relx=0.05,rely=0.65) 
        passwordentry.place(relx=0.30,rely=0.65)

        emaillabel = customtkinter.CTkLabel(self.mainwindow,text="Email:",text_color="#FFFFFF",width=(1535*0.5)*0.19,height=(795*0.9)*0.1125,font=(customtkinter.CTkFont,60)) 

        emailentry = customtkinter.CTkEntry(self.mainwindow,fg_color="transparent",width=(1535*0.5)*0.19,height=(795*0.9)*0.1125) 

        emaillabel.place(relx=0.05,rely=0.85) 
        emailentry.place(relx=0.30,rely=0.85) 


        risksLabel = customtkinter.CTkLabel(self.mainwindow,text="Risk sliders",text_color="#FFFFFF",width=(1535*0.5)*0.19,height=(795*0.9)*0.1)

        lowLock = customtkinter.CTkSwitch(self.mainwindow,height=39.75,width = 95.9375,progress_color="transparent",text="Lock")
        mediumLock = customtkinter.CTkSwitch(self.mainwindow,height=39.75,width = 95.9375,progress_color="transparent",text="Lock") 
        highLock = customtkinter.CTkSwitch(self.mainwindow,height=39.75,width = 95.9375,progress_color="transparent",text="Lock")
        
        
        lowText = customtkinter.CTkLabel(master=self.mainwindow,text="Low risk",width=767.5*0.5,height=39.75,fg_color="transparent")
        mediumText = customtkinter.CTkLabel(master=self.mainwindow,text="Medium risk",width=767.5*0.5,height=39.75,fg_color="transparent")                 
        highText = customtkinter.CTkLabel(master=self.mainwindow,text="High risk",width=767.5*0.5,height=39.75,fg_color="transparent")                          
                                    #20 and 2/3 each 
                                    # 
       
        
        lowNumber = customtkinter.CTkLabel(master=self.mainwindow,text=f"{results[0][0]}%",width=95.9375,height=39.75,fg_color="transparent")
        lowSliderr = customtkinter.CTkSlider(master=self.mainwindow,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSliderr,"medium":mediumSliderr,"high":HighSliderr},slidersInfo,"low",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
        
        mediumNumber = customtkinter.CTkLabel(master=self.mainwindow,text=f"{results[0][1]}%",width=95.9375,height=39.75,fg_color="transparent")
        mediumSliderr = customtkinter.CTkSlider(master=self.mainwindow,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSliderr,"medium":mediumSliderr,"high":HighSliderr},slidersInfo,"medium",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
    
        HighNumber = customtkinter.CTkLabel(master=self.mainwindow,text=f"{results[0][2]}%",width=95.9375,height=39.75,fg_color="transparent")
        HighSliderr = customtkinter.CTkSlider(master=self.mainwindow,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSliderr,"medium":mediumSliderr,"high":HighSliderr},slidersInfo,"high",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
        slidersInfo = {"low":{"LastValue":lowValue,"Text":lowNumber},"medium":{"LastValue":mediumValue,"Text":mediumNumber},"high":{"LastValue":highValue,"Text":HighNumber}}
        
        nextButton = customtkinter.CTkButton(master = self.mainwindow,text="next",command=partial(checkSignupInfo,"",firstname=firstnameentry,secondname=secondnameentry,email=emailentry,password=passwordentry,Username=usernameentry,usedwhen="Alter"))
        
        
        nextButton.place(relx=0.5,rely=0.7)
        lowSliderr.set(results[0][0])
        mediumSliderr.set(results[0][1])
        HighSliderr.set(results[0][2])

        
        
        lowText.place(rely=0.15,relx=0.5)
        lowSliderr.place(relx=0.55,rely=0.225)
        lowNumber.place(relx=0.475,rely=0.225)

        mediumText.place(relx=0.5,rely=0.325)
        mediumSliderr.place(relx=0.55,rely=0.4)
        mediumNumber.place(relx=0.475,rely=0.4) 

        highText.place(relx=0.5,rely=0.5)
        HighSliderr.place(relx=0.55,rely=0.575) 
        HighNumber.place(relx=0.475,rely=0.575)

        lowLock.place(relx=0.9,rely=0.225) 
        mediumLock.place(relx=0.9,rely=0.4) 
        highLock.place(relx=0.9,rely=0.575) 


class MoneyPage(Window): 

    def __init__(self,window):
        super().__init__() 
        self.mainwindow = window.mainwindow 
     
    def initialiseEntries(self): 

        addmoneylabel = customtkinter.CTkLabel(master=self.mainwindow,text="Add money",font=("Helvetica",94))
        addmoneyentrybox = customtkinter.CTkEntry(master=self.mainwindow,fg_color="transparent",height=(795*0.9)*0.2,width=1535*0.25)
        dollarsign = customtkinter.CTkLabel(master=self.mainwindow,text="$",font=("Helvetica",120))
        
        addmoneylabel.place(relx=0.05,rely=0.05)
        addmoneyentrybox.place(relx=0.1,rely=0.27)
        dollarsign.place(relx=0.05,rely=0.25) 

        withdrawmoneylabel = customtkinter.CTkLabel(master=self.mainwindow,text="Withdraw money",font=("Helvetica",74))
        withdrawmoneyentrybox = customtkinter.CTkEntry(master=self.mainwindow,fg_color="transparent",height=(795*0.9)*0.2,width=1535*0.25)
        dollarsignwithdraw = customtkinter.CTkLabel(master=self.mainwindow,text="$",font=("Helvetica",120)) 

        
        withdrawmoneylabel.place(relx=0.05,rely=0.5)
        withdrawmoneyentrybox.place(relx=0.1,rely=0.62)
        dollarsignwithdraw.place(relx=0.05,rely=0.65)
        totalcashlabel = customtkinter.CTkLabel(master=self.mainwindow,text="Total funds",font=("Helvetica",94)) 

        sqlQueryQueue.put((1,"SELECT Funds,Low,Medium,High FROM usersTest2 WHERE id = ?",(engine.currentloggedid,),stocksTwo.cursor))
        
        sqlThread(stocksTwo.con) 

        result = sqlAnswersQueue.get() 
        print(result,engine.currentloggedid)
        totalcashvalue =  customtkinter.CTkLabel(master=self.mainwindow,text=f"{result[0][0]}",font=("Helvetica",94))

        availablecashvaluelabel =  customtkinter.CTkLabel(master=self.mainwindow,text="Available funds (no stocks)",font=("Helvetica",64))

        availablecashvalue =  customtkinter.CTkLabel(master=self.mainwindow,text=f"{result[0][1]+result[0][2]+result[0][3]}",font=("Helvetica",94))
        dollarsigntotal = customtkinter.CTkLabel(master=self.mainwindow,text="$",font=("Helvetica",120)) 
        dollarsignavailable = customtkinter.CTkLabel(master=self.mainwindow,text="$",font=("Helvetica",120))
        totalcashlabel.place(relx=0.5,rely=0.05)
        totalcashvalue.place(relx=0.55,rely=0.22)
        availablecashvaluelabel.place(relx=0.5,rely=0.4) 
        availablecashvalue.place(relx=0.55,rely=0.57)
        dollarsigntotal.place(relx=0.5,rely=0.2) 
        dollarsignavailable.place(relx=0.5,rely=0.55)

        gobutton = customtkinter.CTkButton(master=self.mainwindow,text=f"Apply changes",command=partial(AddorWithdrawmoney,addmoneyentrybox,withdrawmoneyentrybox,result[0][0],(result[0][1]+result[0][2]+result[0][3])),width=1535*0.15,height=(795*0.9)*0.05)
        gobutton.place(relx=0.6,rely=0.8)


class LoginSignupWindow(Window): 

    def __init__(self):
        super().__init__() 
        self.mainwindow = customtkinter.CTkFrame(root,width = 1535,height=795,fg_color="transparent")

    def clearpage(self): 

        self.mainwindow.destroy() 

        self.mainwindow = customtkinter.CTkFrame(root,width = 1535,height=795,fg_color="transparent")
    
        self.mainwindow.place(relx=0,rely=0) 

    def initialisePage(self):
        
        self.mainwindow.place(relx=0,rely=0)


def mainPages(frameToDestroy): 

     
    
    frameToDestroy.destroy()

    
    window = Window() 
    window.makeToolbar()
    window.initialise()
    
    text = customtkinter.CTkLabel(master=window.mainwindow) 
    text.place(relx=0.5,rely=0.5)

def checkLoginInfo(frameToDestroy,usernameEntry,passwordEntry,usernamesignup): 

    username = usernameEntry.get() 
    password = passwordEntry.get() 

    
    if username == usernamesignup: 

        print("THESE ARE THE SAME")
    
    
    print(f"Username:{username},Password:{password}")
    
    if str(username) == "" or str(password) == "": 

        messagebox.showerror(message="Username or password cannot be blank",title="Error") 

    else: 
        hash = hashlib.new("SHA256") 
    
        usernamehashed = hash.update(username.encode())
        usernamehashedhex = hash.hexdigest() 

        hashed_Password = hash.update(password.encode()) 
        hexHashpassword = hash.hexdigest() 
      
        

        sqlQueryQueue.put((1,"SELECT Username,Password,id FROM usersTest2 WHERE Username = ?",(usernamehashedhex,),stocksTwo.cursor))
        sqlThread(con)
    
    
        results = sqlAnswersQueue.get()
        
        
        
        

        
        print(f"Username:{usernamehashedhex},Password:{hexHashpassword}")

        
        if results == []: 

            messagebox.showerror(message="Username not in use",title="Error")
        
        else: 
            
            if results[0][1] == str(hexHashpassword) and results[0][0] == str(usernamehashedhex): 

                 
                currentLoggedInID = results[0][2]
                engine.setloggedid(currentLoggedInID)
                
                mainPages(frameToDestroy) 



            else: 
                messagebox.showerror(message="Username or password incorrect",title="Error")



def login(window,username): 

    window.clearpage()

    mainframe = customtkinter.CTkFrame(window.mainwindow,width=767.5,height=795,fg_color="transparent") 

    entryUsername = customtkinter.CTkEntry(master=mainframe,placeholder_text="Username",height=150,width=700) 
    entryUsername.place(relx=0.06,rely=0.25) 

    entryPassword = customtkinter.CTkEntry(master=mainframe,placeholder_text="Password",height=150,width=700) 
    entryPassword.place(relx=0.06,rely=0.45) 

    enterButton = customtkinter.CTkButton(master=mainframe,text="Enter",height=50,width=200,command=partial(checkLoginInfo,mainframe,entryUsername,entryPassword,username))
    enterButton.place(relx=0.375,rely=0.8) 
    
    mainframe.place(relx=0.25,rely=0)
def decideLoginOrSignup(thingsToDestroy): 
    
    
    
    
    window = LoginSignupWindow()
    window.initialisePage()
    
    
    

    loginButton = customtkinter.CTkButton(master=window.mainwindow,text="Login",width = 700,height=200,font=("CTkFont",60),command=partial(login,window)) 
    loginButton.place(relx=0.25,rely=0.3)
    signupButton = customtkinter.CTkButton(master=window.mainwindow,command=partial(signup,window),text="Signup",width = 700,height=200,font=("CTkFont",60))
    signupButton.place(relx=0.25,rely=0.6)



def signup(window): 
    
    
    window.clearpage()
    
    
    
    
    
    nameframe = customtkinter.CTkFrame(master=window.mainwindow,height=80,width=600,fg_color="transparent")
    

    otherinfoframe =  customtkinter.CTkFrame(master=window.mainwindow,height=320,width=600,fg_color="transparent")
    
    
    
    
    
    
    
    
    entryFirstname = customtkinter.CTkEntry(master=nameframe,placeholder_text="First name",height=50,width=150) 
    entryFirstname.place(relx=0.2,rely=0.5) 
    
    entrySecondname = customtkinter.CTkEntry(master=nameframe,placeholder_text="Last name",height=50,width=150) 
    entrySecondname.place(relx=0.5,rely=0.5) 
    
    entryUsername = customtkinter.CTkEntry(master=otherinfoframe,placeholder_text="Username",height=50,width=330) 
    entryUsername.place(relx=0.35,rely=0.05) 

    entryemail = customtkinter.CTkEntry(master=otherinfoframe,placeholder_text="Email Address",height=50,width=330) 
    entryemail.place(relx=0.35,rely=0.25) 
    
    entryPassword = customtkinter.CTkEntry(master=otherinfoframe,placeholder_text="Password",height=50,width=330) 
    entryPassword.place(relx=0.35,rely=0.45) 

    
    enterButton = customtkinter.CTkButton(master=otherinfoframe,text="Enter",command=partial(checkSignupInfo,window,firstname=entryFirstname,secondname=entrySecondname,email=entryemail,password=entryPassword,Username=entryUsername,usedwhen="Signup"),height=50,width=200)
    enterButton.place(relx=0.45,rely=0.8) 

    nameframe.place(x=470,y=220)
    otherinfoframe.place(x=380,y=300)
    
    
    # backButton = customtkinter.CTkButton(master=backFrame,text="Back",command=partial(decideLoginOrSignup,[entryUsername,entryPassword,enterButton,frame]),height=75,width=300)
    # backButton.pack()
    
def checkSignupInfo(window,firstname,secondname,email,password,Username,usedwhen): 
    hash = hashlib.new("SHA256") 
    
    usernamehashed = hash.update(Username.get().encode())
    usernamehashedhex = hash.hexdigest() 

    
    
    
    
    
    sqlQueryQueue.put((1,"SELECT Username FROM usersTest2 WHERE Username = ?",(f'{str(usernamehashedhex)}',),stocksTwo.cursor))
    sqlThread(con)
    
    # cursor.execute("SELECT Username FROM usersTest2 WHERE Username = ?",(f'{str(usernamehashedhex)}',))
    resultsUsername = sqlAnswersQueue.get()
    print(resultsUsername)
    errorMessage = ""
    
    if str(resultsUsername) != "[]": 
        
        errorMessage += "\nUsername already in use"
    
   
    emailhashed = hash.update(f"{email.get()}".encode())
    emailhashedhex = hash.hexdigest() 
    
    sqlQueryQueue.put((1,"SELECT email FROM usersTest2 WHERE email = ?",(str(emailhashedhex),),stocksTwo.cursor))
    sqlThread(con)
    
    # cursor.execute("SELECT email FROM usersTest2 WHERE email = ?",(f'{str(emailhashedhex)}',))
    resultsEmail = sqlAnswersQueue.get()
    print(resultsEmail)
    if str(resultsEmail) != "[]": 
        
        errorMessage += "\nEmail address already in use"
    
    
    if errorMessage == "": 

        userInfo = {"firstname":"","password":"","email":"","username":"","secondname":"","firstnamehashed":"","passwordhashed":"","emailhashed":"","usernamehashed":"","secondnamehashed":""}
        
        hashed_firstname = hash.update(f"{firstname.get()}".encode()) 
        hexHashName = hash.hexdigest() 
        userInfo["firstname"] = firstname.get()
        userInfo['firstnamehashed'] = str(hexHashName)
        hashed_secondname = hash.update(f"{secondname.get()}".encode()) 
        hexHashName = hash.hexdigest() 
        userInfo["secondname"] = secondname.get() 
        userInfo['secondnamehashed'] = hexHashName
        hashed_email = hash.update(f"{email.get()}".encode()) 
        hexHashName = hash.hexdigest() 
        userInfo["email"] = email.get() 
        userInfo["emailhashed"] = str(hexHashName)
        hashed_Username = hash.update(f"{Username.get()}".encode()) 
        hexHashName = hash.hexdigest() 
        userInfo["username"] = Username.get() 
        userInfo['usernamehashed'] = hexHashName
        hashed_Password = hash.update(f"{password.get()}".encode()) 
        hexHashName = hash.hexdigest() 
        userInfo["password"] = password.get()
        userInfo['passwordhashed'] = hexHashName
        
        
        if usedwhen == "Signup":
            initialMoney(window,userInfo) 

        else: 

            sqlQueryQueue.put((1,"UPDATE usersTest2 SET Firstname=?,Password=?,email=?,Username=?,Secondname=? WHERE id=?",(userInfo['firstnamehashed'],userInfo['passwordhashed'],userInfo["usernamehashed"],userInfo["emailhashed"],userInfo["secondnamehashed"],engine.currentloggedid,),cursor))
            sqlThread(con) 
            sqlAnswersQueue.get()
            print("Update has been complete")
    
    else: 
        print(errorMessage)
        messagebox.showerror('Error',errorMessage)

def monatization(window): 

    window.clearMainpage()
    
    mp = MoneyPage(window)
    mp.initialiseEntries()



def changeSliders(sliderActual,sliders,whatchanged,value,textt,locks): 
    max = 100
    sliderNames = ["low","medium","high"]
    
    sliderNames.remove(whatchanged)
    
    checks = 0 
    i=0
    while checks < 2: 
        
        item = sliderNames[i] 
        
        if locks[item].get() == 1: 

            sliderNames.remove(item)
            max = max-round(conversionsForValues[item])
            
            
            
            checks += 1
        
        
        else: 
            i = i + 1
            checks +=1
    
    
    
    
    if locks[whatchanged].get() == 1: 

        sliderActual[whatchanged].set(conversionsForValues[item])
    
    
    
    else: 
        
        if round(value,0) == conversionsForValues[whatchanged]: 

            pass 

        else: 
            
            
            
            if len(sliderNames) == 1: 
                
                if value >= max: 
        
        
                    conversionsForValues[whatchanged] = max 
                    conversionsForValues[sliderNames[0]] = 0
                
                else:
                    conversionsForValues[whatchanged] = round(value,0)
                    conversionsForValues[sliderNames[0]]= max-round(value,0) 

                    
                    
                    
            
            elif len(sliderNames) == 0: 
                
                
                
                sliderActual[whatchanged].set(conversionsForValues[whatchanged]) 
                 
                
                
                textt[whatchanged].configure(text=f"{conversionsForValues[whatchanged]}%")
            
            
            else: 
                difference = max - value 
                
                option1 = sliderNames[0] 
                option2 = sliderNames[1] 
                textt[whatchanged].configure(text=f"{value}%")
                
                
                
                sliderActual[option1].set(difference/2) 
                sliderActual[option2].set(difference/2) 
                conversionsForValues[option1] = difference/2 
                conversionsForValues[option2] = difference/2 
                textt[option1].configure(text=f"{(difference/2)}%") 
                textt[option2].configure(text=f"{(difference/2)}%")

                sliderActual[whatchanged].set(value)
                conversionsForValues[whatchanged] = 100 - (conversionsForValues[othertwo[whatchanged][0]] + conversionsForValues[othertwo[whatchanged][1]] )

    sliderActual['low'].set(conversionsForValues['low']) 
    textt['low'].configure(text=f"{conversionsForValues['low']}%")
    sliderActual['medium'].set(conversionsForValues['medium']) 
    textt['medium'].configure(text=f"{conversionsForValues['medium']}%") 
    sliderActual['high'].set(conversionsForValues['high']) 
    textt['high'].configure(text=f"{conversionsForValues['high']}%")
    
def initialMoney(window,userInfo): 
    
    
    global lowSlider 
     
    global mediumSlider 
     
    global HighSlider
    
    window.clearpage()
    
                         #795 height x 1535 width
    big = customtkinter.CTkFrame(window.mainwindow,width=1535,height=795,fg_color="transparent")
    mainframe = customtkinter.CTkFrame(window.mainwindow,width=767.5,height=795,fg_color="transparent")
    
    fundsQuestion = customtkinter.CTkLabel(master=mainframe,text="How much would you like to deposit?",width=767.5,height=59.625,fg_color="transparent",font=("Helvetica",40))
    fundsEntryBox = customtkinter.CTkEntry(master=mainframe,height=59.625,width=383.75,fg_color="transparent",font=('Helvetica',60))
    dollarsign = customtkinter.CTkLabel(master=mainframe,height=56.625,width=76.725,text="$",font=('Helvetica',80),fg_color="transparent")
    
    AllocationText = customtkinter.CTkLabel(master=mainframe,text="How would you like your funds allocated?",width=767.5,height=59.625,fg_color="transparent",font=("Helvetica",40))
    
    lowLock = customtkinter.CTkSwitch(mainframe,height=39.75,width = 95.9375,progress_color="transparent",text="Lock")
    mediumLock = customtkinter.CTkSwitch(mainframe,height=39.75,width = 95.9375,progress_color="transparent",text="Lock") 
    highLock = customtkinter.CTkSwitch(mainframe,height=39.75,width = 95.9375,progress_color="transparent",text="Lock")
    
    
    lowText = customtkinter.CTkLabel(master=mainframe,text="Low",width=767.5,height=39.75,fg_color="transparent")
                                #20 and 2/3 each 
                                # 
    lowNumber = customtkinter.CTkLabel(master=mainframe,text="34%",width=95.9375,height=39.75,fg_color="transparent")
    mediumNumber = customtkinter.CTkLabel(master=mainframe,text="33%",width=95.9375,height=39.75,fg_color="transparent")
    HighNumber = customtkinter.CTkLabel(master=mainframe,text="33%",width=95.9375,height=39.75,fg_color="transparent")
    
    lowSlider = customtkinter.CTkSlider(master=mainframe,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSlider,"medium":mediumSlider,"high":HighSlider},slidersInfo,"low",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
    
    
    mediumSlider = customtkinter.CTkSlider(master=mainframe,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSlider,"medium":mediumSlider,"high":HighSlider},slidersInfo,"medium",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
   
    
    HighSlider = customtkinter.CTkSlider(master=mainframe,height=39.75,width=498.875,from_=0,to=100,number_of_steps=100,command=lambda value: changeSliders({"low":lowSlider,"medium":mediumSlider,"high":HighSlider},slidersInfo,"high",value,{"low":lowNumber,"medium":mediumNumber,"high":HighNumber},{"low":lowLock,"medium":mediumLock,"high":highLock}))
    slidersInfo = {"low":{"LastValue":lowValue,"Text":lowNumber},"medium":{"LastValue":mediumValue,"Text":mediumNumber},"high":{"LastValue":highValue,"Text":HighNumber}}
    
    nextButton = customtkinter.CTkButton(master = big,text="next",command=partial(finisherPage,window,userInfo=userInfo,fundsData={"totalfunds":fundsEntryBox,"low":lowSlider,"medium":mediumSlider,"high":HighSlider}))
    
    
    
    lowSlider.set(34)
    mediumSlider.set(33.5)
    HighSlider.set(33.5)

    big.place(relx=0,rely=0)
    mainframe.place(relx=0.25,rely=0)
    fundsQuestion.place(relx=0,rely=0.01)
    fundsEntryBox.place(relx=0.3,rely=0.109)
    dollarsign.place(relx=0.2,rely=0.1)
    AllocationText.place(relx=0,rely=0.25)
    nextButton.place(relx=0.9,rely=0.5)
    lowText.place(rely=0.35,relx=0)
    lowSlider.place(relx=0.175,rely=0.425)
    lowNumber.place(relx=0.025,rely=0.425)

    mediumSlider.place(relx=0.175,rely=0.6)
    mediumNumber.place(relx=0.025,rely=0.6) 

    HighSlider.place(relx=0.175,rely=0.775) 
    HighNumber.place(relx=0.025,rely=0.775)

    lowLock.place(relx=0.85,rely=0.425) 
    mediumLock.place(relx=0.85,rely=0.6) 
    highLock.place(relx=0.85,rely=0.775)


def insertuserintodatabase(window,userInfo,totalfunds,fundsData): 
    
    lowvalue = float(totalfunds) * float(fundsData['low'].get()/100)
    mediumvalue = float(totalfunds) * float(fundsData['medium'].get()/100)
    highvalue = float(totalfunds) * float(fundsData['high'].get()/100)
    
    
    print(f"USERNAME: {userInfo['username']},PASSWORD: {userInfo['password']}")



    hash = hashlib.new("SHA256") 
    
    
    firstnamehashed = hash.update(f"{userInfo['firstname']}".encode())
    firstnamehashedhex = hash.hexdigest() 

    secondnamehashed = hash.update(f"{userInfo['secondname']}".encode())
    secondnamehashedhex = hash.hexdigest() 

    emailhashed = hash.update(f"{userInfo['email']}".encode())
    emailhashedhex = hash.hexdigest() 
    
    
    usernamehashed = hash.update(f"{userInfo['username']}".encode())
    usernamehashedhex = hash.hexdigest() 

    hashed_Password = hash.update(f"{userInfo['password']}".encode()) 
    hexHashpassword = hash.hexdigest()
    
    
    print(usernamehashedhex,hexHashpassword)
    
    
    sqlQueryQueue.put((1,"INSERT INTO usersTest2(email,Firstname,Secondname,Password,Username,Funds,Low,Medium,High,LowPercentage,MediumPercentage,HighPercentage,Lowdefecit,Mediumdefecit,Highdefecit) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0,0,0)",(emailhashedhex,firstnamehashedhex,secondnamehashedhex,hexHashpassword,usernamehashedhex,totalfunds,lowvalue,mediumvalue,highvalue,fundsData['low'].get(),fundsData['medium'].get(),fundsData['high'].get(),),stocksTwo.cursor))
    sqlThread(con) 
    sqlAnswersQueue.get()

    sqlQueryQueue.put((1,"SELECT Username,Password FROM usersTest2",(),stocksTwo.cursor))
    sqlThread(con) 
    print(sqlAnswersQueue.get()[1])
    
    
    
    login(window,userInfo['username'])

def finisherPage(window,userInfo,fundsData): 
    totalfunds = fundsData['totalfunds'].get()
    
    window.clearpage()

    
    mainframe = customtkinter.CTkFrame(window.mainwindow,width=767.5,height=795,fg_color="transparent")
    finalStepText = customtkinter.CTkLabel(mainframe,text="Almost Finished!!",height=59.625,width=767.5,font=("Helvetica",40),fg_color="transparent")
    checkInfoText = customtkinter.CTkLabel(mainframe,text="Check to see we have your information correct before",height=59.625,width=767.5,font=("Helvetica",32),fg_color="transparent")
    continuing = customtkinter.CTkLabel(mainframe,text="continuing",height=59.625,width=767.5,font=("Helvetica",32),fg_color="transparent")
    
    nameText =customtkinter.CTkLabel(mainframe,text=f"Name : {userInfo['firstname']} {userInfo['secondname']}",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    usernameText =customtkinter.CTkLabel(mainframe,text=f"Username : {userInfo['username']}",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    emailText =customtkinter.CTkLabel(mainframe,text=f"Email : {userInfo['email']}",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    passwordText =customtkinter.CTkLabel(mainframe,text=f"Password : {userInfo['password']}",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    fundsText =customtkinter.CTkLabel(mainframe,text=f"Total funds : £{totalfunds}",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    lowText =customtkinter.CTkLabel(mainframe,text=f"Low : {fundsData['low'].get()}%",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    mediumText =customtkinter.CTkLabel(mainframe,text=f"Medium : {fundsData['medium'].get()}%",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")
    highText =customtkinter.CTkLabel(mainframe,text=f"High : {fundsData['high'].get()}%",height=59.625,width=767.5,font=("Helvetica",25),fg_color="transparent")

    
    
    
    
    
    
    nextButton = customtkinter.CTkButton(master = root,text="next",command=partial(insertuserintodatabase,window,userInfo,totalfunds,fundsData))
    
    
    mainframe.place(relx=0.25,rely=0)
    finalStepText.place(relx=0,rely=0.01)
    checkInfoText.place(relx=0.01,rely=0.15)
    continuing.place(relx=0.0,rely=0.185)
    nameText.place(relx=0,rely=0.25)
    usernameText.place(relx=0,rely=0.30)
    emailText.place(relx=0,rely=0.35) 
    passwordText.place(relx=0,rely=0.40)
    fundsText.place(relx=0,rely=0.45) 
    lowText.place(relx=0,rely=0.50) 
    mediumText.place(relx=0,rely=0.55) 
    highText.place(relx=0,rely=0.60)
    nextButton.place(relx=0.9,rely=0.5)






def emailNotifications(thingsToDelete):
    
    
    for thing in thingsToDelete: 
        
        thing.destroy()

    mainframe = customtkinter.CTkFrame(root,width=767.5,height=795,fg_color="transparent")
    notificationQuestionFrame = customtkinter.CTkFrame(mainframe,width=690.75,height=238.5,fg_color="transparent")
    
    
    emailnotisText = customtkinter.CTkLabel(notificationQuestionFrame,text="Do you want to recieve email notifications?")
    
    emailnotis = customtkinter.CTkSwitch(notificationQuestionFrame,text="")
    yesNoText = customtkinter.CTkLabel(notificationQuestionFrame,text=f"{emailnotis.get()}")
    
    mainframe.place(relx=0.25,rely=0)
    notificationQuestionFrame.place(relx=0.05,rely=0.05)
    emailnotis.place(relx=0.5,rely=0.8)
    emailnotisText.place(relx=0.3,rely=0.2) 
    yesNoText.place(relx=0.5,rely=0.5)
pointer = 0




frame = customtkinter.CTkFrame(root,width=600,height=400,bg_color="transparent",fg_color="transparent") 

 
print("Starting things up")

decideLoginOrSignup([])


root.mainloop()


