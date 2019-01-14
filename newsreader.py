import tkinter as tk
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
import time
from threading import Thread

# Parameters for news source and update period (in seconds).
# Change updatePeriod for adjusting time period of checking news updates
rssUrl = "https://timesofindia.indiatimes.com/rss.cms"
updatePeriod = 60

# -----------------------------------------------------------------

# Function for retrieving top story for a given category name and its RSS url.
# Error in parsing the category url (due to temporary non-availability of news) is managed with try-except
def getTopStory(url, categoryName):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features = 'xml')
    item = soup.find('item')
    try:
        return categoryName, item.title.string
    except AttributeError:
        return categoryName, 'ERROR: NEWS ITEM NOT FOUND.'

# -------------------------------------------------------------------

# Connect with the newsfeed url and parse it
data = requests.get(rssUrl)
soup = BeautifulSoup(data.text, features = "html.parser")
storyList = {}

categoryList = soup.find(width = "640", border = "0").find_all('tr')
masterList = []

# Get category names and respective urls
for category in categoryList:
    linkTag = category.td.a
    masterList.append((linkTag.string, linkTag.get('href')))

# Get top story from each category
for category in masterList:
    story = getTopStory(category[1], category[0])
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

    # Creates the category labels and the update status label
    def createLabels(self):
        for i in range(20):
            blank1 = tk.Label(self, text=' ')
            blank2 = tk.Label(self, text=' ')
            blank1.grid(row=0, column=0)
            blank2.grid(row=2, column=0)
            self.categoryLabels.append(tk.Label(self, text='\t'+masterList[i][0]+'   |   ', font='Manjari 18 bold'))
            self.categoryLabels[i].grid(row=i+3, column=0, sticky=tk.E)
            self.statusLabel = tk.Label(self, text='Newsreader', font='Manjari 15 italic')
            self.statusLabel.grid(row=1, column=1)
    
    # Creates the news labels
    def createNewsLabels(self):
        for i in range(20):
            self.newsLabels.append(tk.Label(self, text=storyList[masterList[i][0]], font='Manjari 18'))
            self.newsLabels[i].grid(row=i+3, column=1, sticky=tk.W)
    
    # Starts an infinite loop that checks for updates periodically
    def updateLoop(self):
        global storyList
        while True:
            time.sleep(updatePeriod)
            self.statusLabel.config(text='Getting updates...')
            for i in range(20):
                category = masterList[i]
                newStory = getTopStory(category[1], category[0])
                if newStory[1] != storyList[category[0]]:
                    storyList[newStory[0]] = newStory[1]
                    self.newsLabels[i].config(text=newStory[1])
            statusStr = 'Last update: ' + dt.now().strftime('%H : %M : %S')
            self.statusLabel.config(text=statusStr)

    # Function to initiate a new thread that runs the updateLoop process.
    def initiate(self):
        self.newsThread = Thread(target=self.updateLoop)
        self.newsThread.daemon = True # Daemon thread - will terminate automatically when GUI window is closed
        self.newsThread.start()


app = Application()
app.master.geometry("1500x800")
app.master.title('Newsreader')
app.mainloop()


