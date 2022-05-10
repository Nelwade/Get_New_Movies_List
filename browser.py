from selenium import webdriver
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

import chromedriver_autoinstaller
import time

chromedriver_autoinstaller.install () # automatically installs chromedriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(
    "--user-data-dir=C:\\Users\\Stewie\\AppData\\Local\\Google\\Chrome\\User Data"
    )
driver = webdriver.Chrome(chrome_options=options) 
driver.implicitly_wait(1)

def notification(message, duration):
    notification = ToastNotifier()
    return notification.show_toast('New Movies', message, duration=duration)


def get_list():
    movie_list =[]
    driver.get('https://yts.mx/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # recent = soup.find_all('div', class_= "browse-movie-wrap col-xs-10 col-sm-5")
    recent = soup.find_all('div', class_ = 'browse-movie-bottom')

    for movie in recent[:4]:
        movie= movie.text
        movie = movie.split('\n')
        movie = ' '.join(movie for movie in movie)
        notification(str(movie), 10)
        movie_list.append(movie.strip())

notification("New Movies Running..", 5)
get_list()