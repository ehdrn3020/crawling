from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Crawling(QThread):
    getNews = pyqtSignal(str, str)

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        ### 자동화된 소프트웨어 제어되고 있다는 문구 제거
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.crawlNews(driver)
        driver.quit()

    def crawlNews(self, driver):
        driver.get('https://news.naver.com/main/ranking/popularDay.naver')
        ### 암묵적으로 웹 자원 로드를 위해 3초 대기
        driver.implicitly_wait(1)

        # return value
        for i in range(1,13):
            t = driver.find_element(by=By.XPATH, value=f'//*[@id="wrap"]/div[4]/div[2]/div/div[{i}]/a/strong').text
            self.getNews.emit('','\n['+t+']')
            for j in range(1,6):
                xpath = driver.find_element(by=By.XPATH, value=f'//*[@id="wrap"]/div[4]/div[2]/div/div[{i}]/ul/li[{j}]/div/a')
                link = xpath.get_attribute('href')
                news_letter = xpath.text

                print(link, news_letter)
                self.getNews.emit(link, news_letter)
