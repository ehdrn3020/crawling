import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGridLayout, QLabel, QPushButton, QTextBrowser
from crawl import Crawling

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel('크롤링:'), 0, 0)
        grid.addWidget(QLabel('리스트:'), 1, 0)

        self.startBtn = QPushButton('시작')
        grid.addWidget(self.startBtn, 0, 1)

        self.newsText = QTextBrowser()
        grid.addWidget(self.newsText, 1, 1)
        #서식있는 텍스트(Richtext)를 사용 가능
        self.newsText.setAcceptRichText(True)
        # 외부링크로 연결 가능
        self.newsText.setOpenExternalLinks(True)

        self.setWindowTitle('Naver News Collector')
        self.moveCenter()
        self.resize(600, 700)
        self.show()

        # 버튼 클릭시 크롤링 이벤트
        self.startBtn.clicked.connect(self.startCrawl)

    # 화면가운데로 띄우기
    def moveCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 크롤링 시작
    def startCrawl(self):
        self.startBtn.setText('시작')
        x = Crawling(self)
        x.start()
        x.getNews.connect(self.writeNews)

    def writeNews(self, link, news):
        if link == '':
            self.newsText.append(news)
        else :
            self.newsText.append(f'<a style="color:black;text-decoration:none;" href="{link}">{news}</a>')

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())