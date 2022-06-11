from selenium import webdriver
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from win10toast_click import ToastNotifier
from winotify import Notification

import chromedriver_autoinstaller
import time

chromedriver_autoinstaller.install () # automatically installs chromedriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(
    "--user-data-dir=C:\\Users\\Stewie\\AppData\\Local\\Google\\Chrome\\User Data"
    )
driver = webdriver.Chrome(chrome_options=options) 
driver.implicitly_wait(10)

def winotification(movie, trailer_link, download_link):
    toast = Notification(
        app_id = "Python",
        title = "New Movies",
        msg = movie
    )
    toast.add_actions(
        label="Trailer", 
        launch=trailer_link
        )

    toast.add_actions(
        label="Download", 
        launch=download_link
    )
    toast.show()

# def notification(message):
#     notification = ToastNotifier()
#     return notification.show_toast('New Movies', message, duration=None)

# def notification_click(message):
#     notification = ToastNotifier()
#     return notification.show_toast('New Movies', message, duration=5, threaded=True)


def parse_html(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_list():
    movie_list =[]
    soup = parse_html('https://yts.mx/')
    recent = soup.find_all('div', class_ = 'browse-movie-bottom')

    for movie in recent[:4]:
        movie_link = movie.find('a', class_ = "browse-movie-title")['href']
        movie = movie.text
        movie = movie.split('\n')
        movie = ' '.join(movie for movie in movie)
        #notification_click(str(movie))
        # movie_list.append(movie.strip())

        #winotification(str(movie))

        soup = parse_html(movie_link)
        details = soup.find("div", id="movie-info" )
        description = details.find("div", class_= "hidden-xs").text
        print("\nMovie Description: ", description)
        
        # download_link = details.find("div", class_="hidden-xs hidden-sm")
        
        try:
            download_link = details.find("a", string="1080p.WEB")["href"]
        except:
            try:
                download_link = details.find("a", string="720p.WEB")["href"]
            except:
                download_link = details.find("a", string="2160p.WEB")["href"]

        print("Donwload Link: ", download_link)
        print()

        rating = details.find("span", itemprop = "ratingValue").text
        print("IMDB Rating: ", rating)
        print()

        trailer_link = soup.find("a", class_="youtube cboxElement")["href"]
        print("Watch trailer at: ", trailer_link)
        print()

        winotification(movie, trailer_link, download_link)
        print("yippee")
        

# notification_click("New Movies Running..")
get_list()
driver.close()
driver.quit()
