from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
from python_elements import *
from functools import partial

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

        addcontainer = QWidget()
        addbox = QVBoxLayout()
        addcontainer.setLayout(addbox)

        for section in all_elements.keys():
            label = QLabel()
            label.setText(section)
            font = self.font()
            font.setPixelSize(16)
            font.setBold(True)
            label.setFont(font)
            addbox.addWidget(label)
            for element in all_elements[section]:
                addbtn = QPushButton()
                addbtn.setText(element.friendly_name)
                addbtn.setStyleSheet('margin-left: 8px;')
                addbtn.pressed.connect(partial(self.add_element, element))
                addbox.addWidget(addbtn)
        
        addview = QScrollArea()
        addview.setWidget(addcontainer)
        toolbox.addWidget(addview)

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

    def add_element(self, element: type[Element]):
        new_element = element()
        new_element.properties_inside_tag['id'] = f'{element.kind[1:-1]}{len(self.elements)}'
        self.elements.append(new_element)
        self.render_html_content()

    def render_html_content(self):
        f = open('translator.html')
        r = f.read()
        top = r[:r.index('%addarea%')]
        bottom = r[r.index('%addarea%')+len('%addarea%'):]
        f.close()
        middle = ''
        for element in self.elements:
            middle += element.to_html() + '\n'
        self.html.setHtml(top + middle + bottom)

    def element_clicked(self):
        if self.html.title() != 'default-title' and self.html.title() != 'about:blank':
            if self.html.title() != 'parentofelements':
                self.ename.setText(self.html.title())

window = MainWindow()
window.show()
app.exec()