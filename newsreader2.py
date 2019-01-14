import tkinter as tk
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
import notify2
import time
from threading import Thread

rssUrl = "https://timesofindia.indiatimes.com/rss.cms"
updatePeriod = 60

# -----------------------------------------------------------------

def getTopStory(url, categoryName):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features = 'xml')
    item = soup.find('item')
    try:
        return categoryName, item.title.string
    except AttributeError:
        return categoryName, 'ERROR: NEWS ITEM NOT FOUND.'

def notify(title, message):
    notify2.init("Newsreader")
    notice = notify2.Notification(title, message)
    notice.show()
    return

# -------------------------------------------------------------------

data = requests.get(rssUrl)
soup = BeautifulSoup(data.text, features = "html.parser")
storyList = {}

categoryList = soup.find(width = "640", border = "0").find_all('tr')
masterList = []

for category in categoryList:
    linkTag = category.td.a
    masterList.append((linkTag.string, linkTag.get('href')))

for category in masterList:
    story = getTopStory(category[1], category[0])
    # printStory(story[0], story[1])
    storyList[story[0]] = story[1]

# -------------------------------------------------------------------

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.newsThread = None
        self.statusLabel = None
        self.categoryLabels = []
        self.newsLabels = []
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createLabels()
        self.createNewsLabels()
        self.initiate()


    def createLabels(self):
        for i in range(20):
            blank1 = tk.Label(self, text=' ')
            blank2 = tk.Label(self, text=' ')
            blank1.grid(row=0, column=0)
            blank2.grid(row=2, column=0)
            self.categoryLabels.append(tk.Label(self, text='\t'+masterList[i][0]+'   |   ', font='Manjari 18 bold'))
            self.categoryLabels[i].grid(row=i+3, column=0, sticky=tk.E)
            self.statusLabel = tk.Label(self, text='Awaiting update', font='Manjari 15 italic')
            self.statusLabel.grid(row=1, column=1)

    def createNewsLabels(self):
        for i in range(20):
            self.newsLabels.append(tk.Label(self, text=storyList[masterList[i][0]], font='Manjari 18'))
            self.newsLabels[i].grid(row=i+3, column=1, sticky=tk.W)

    def updateLoop(self):
        global storyList
        while True:
            time.sleep(updatePeriod)
            for i in range(20):
                category = masterList[i]
                newStory = getTopStory(category[1], category[0])
                if newStory[1] != storyList[category[0]]:
                    notify(newStory[0], newStory[1])
                    storyList[newStory[0]] = newStory[1]
                    self.newsLabels[i].config(text=newStory[1])
            statusStr = 'Last update: ' + dt.now().strftime('%H : %M : %S')
            self.statusLabel.config(text=statusStr)

    def initiate(self):
        self.newsThread = Thread(target=self.updateLoop)
        self.newsThread.daemon = True
        self.newsThread.start()


app = Application()
app.master.geometry("1500x800")
app.master.title('Newsreader v1.0')
app.mainloop()


