# newsreader
A Python script that scrapes an online RSS feed for top news, and displays it in a Tkinter-based GUI application. Also, periodically checks for any news updates.

## Details
1. The RSS feed used is [Times Of India RSS Feed](https://timesofindia.indiatimes.com/rss.cms). This url is defined at the beginning of the script.
2. The program checks for news updates every minute. This time period is defined at the beginning of the script.

## Libraries used
#### 1. requests
For establishing connection with the online feed and retrieving HTML and XML text.
#### 2. beautifulsoup4
Parses HTML and XML text to obtain the top news items from various categories.
#### 3. tkinter
The GUI toolkit included with Python.
#### 4. threading
Required for background news checking in parallel to the GUI mainloop.

# newsreader2
Has the additional feature of notifying the user via a desktop notification.
###### Note that you need dbus and its dependencies for the notifications.
