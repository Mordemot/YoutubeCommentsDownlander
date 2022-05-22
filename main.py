from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time


def Scrap(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    comment_main = soup.select("#author-text")
    comment_content = soup.select("#content #content-text")
    # here we extract only author nicknames in text from previous downloaded html file and split it to strings list
    # for every comment because of strange bug that add a lot of unnecessary spaces in string
    comment_main = [x.text.split() for x in comment_main]
    # then we connect these lists to one string with proper spaces
    for x in range(len(comment_main)):
        s = " "
        comment_main[x] = s.join(comment_main[x])
        # here we extract comments content in text
    comment_list = [x.text for x in comment_content]
    # check if number of authors and comments content are equal
    if len(comment_content) == len(comment_main):
        for i in range(len(comment_main)):
            print(f"{comment_main[i]} says:")
            print(comment_list[i])
            print('')


def ScrapComment(url):
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=option)
    driver.get(url)
    time.sleep(7)
    driver.execute_script("window.scrollTo(0,400)")
    time.sleep(1)

    # code from stackoverflow to scroll a page with infinite loading
    pause_time = 1  # increase this value if you have slow internet
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        time.sleep(pause_time)
        if new_height == last_height:
            break
        last_height = new_height

    Scrap(driver)


if __name__ == "__main__":
    print("Paste below a link to youtube video: ")
    ScrapComment(input())
