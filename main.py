from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
from python_elements import *

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('ASimpleWYSIWIGEditor')

        self.elements: list[Element] = []

        maincontainer = QWidget()
        mainbox = QHBoxLayout()
        maincontainer.setLayout(mainbox)

        toolbox = QVBoxLayout()
        toolbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        toolcontainer = QWidget()
        toolcontainer.setLayout(toolbox)

        ttitle = QLabel()
        font = self.font()
        font.setPixelSize(24)
        font.setBold(True)
        ttitle.setFont(font)
        ttitle.setText('Toolbox')
        toolbox.addWidget(ttitle)

        testbtn = QPushButton()
        testbtn.setText('Add <h1>')
        testbtn.pressed.connect(self.test_add)
        toolbox.addWidget(testbtn)

        mainbox.addWidget(toolcontainer)

        html = QWebEngineView()
        html.titleChanged.connect(self.element_clicked)
        self.html = html
        self.render_html_content()
        mainbox.addWidget(html)

        properties_container = QWidget()
        properties = QVBoxLayout()
        properties.setAlignment(Qt.AlignmentFlag.AlignTop)
        properties_container.setLayout(properties)

        ptitle = QLabel()
        font = self.font()
        font.setPixelSize(24)
        font.setBold(True)
        ptitle.setFont(font)
        ptitle.setText('Properties')
        properties.addWidget(ptitle)

        ename = QLabel()
        ename.setText('Select an element')
        self.ename = ename
        properties.addWidget(ename)

        mainbox.addWidget(properties_container)

        self.setCentralWidget(maincontainer)

    def test_add(self):
        newh1 = Sh1()
        text = Text()
        text.text = 'New header'
        newh1.properties_inside_tag['id'] = f'newh1-{len(self.elements)}'
        newh1.contains.append(text)
        self.elements.append(newh1)
        self.render_html_content()

    def render_html_content(self):
        f = open('translator.html')
        r = f.read()
        top = r[:r.index('%addarea%')]
        bottom = r[r.index('%addarea%')+len('%addarea%'):]
        f.close()
        middle = ''
        for element in self.elements:
            middle += element.to_html()
        self.html.setHtml(top + middle + bottom)

    def element_clicked(self):
        if self.html.title() != 'default-title' and self.html.title() != 'about:blank':
            if self.html.title() != 'parentofelements':
                self.ename.setText(self.html.title())

window = MainWindow()
window.show()
app.exec()