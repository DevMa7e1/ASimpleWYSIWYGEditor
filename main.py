from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, \
QLabel, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem
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
        self.lookup: dict[str, Element] = {}
        self.last_good_title = None
        self.automated_activity = False

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

        paddbtn = QPushButton()
        paddbtn.setText('Add new...')
        paddbtn.pressed.connect(self.add_row)
        properties.addWidget(paddbtn)

        ptable = QTableWidget()
        ptable.setFixedWidth(213)
        ptable.setRowCount(1)
        ptable.setColumnCount(2)
        ptable.setHorizontalHeaderLabels(['name', 'value'])
        ptable.cellChanged.connect(self.update_element)
        self.ptable = ptable
        properties.addWidget(ptable)

        mainbox.addWidget(properties_container)

        self.setCentralWidget(maincontainer)

    def add_row(self):
        self.ptable.setRowCount(self.ptable.rowCount()+1)

    def update_element(self):
        if not self.automated_activity:
            if self.last_good_title != None:
                self.automated_activity = True
                element = self.lookup[self.last_good_title]
                _id = element.properties_inside_tag['id']
                element.properties_inside_tag.clear()
                element.properties_inside_tag['id'] = _id
                for i in range(self.ptable.rowCount()):
                    name = self.ptable.item(i, 0)
                    value = self.ptable.item(i, 1)
                    if type(name) == QTableWidgetItem and type(value) == QTableWidgetItem:
                        if name.text() != 'id':
                            element.properties_inside_tag[name.text()] = value.text()
                            self.render_html_content()
                        else:
                            newitem = QTableWidgetItem()
                            newitem.setText(element.properties_inside_tag['id'])
                            self.ptable.setItem(i, 1, newitem)
                    elif type(name) != QTableWidgetItem:
                        self.ptable.removeRow(i)
                    elif type(name) == QTableWidgetItem and type(value) != QTableWidgetItem:
                        if name.text() != 'id':
                            element.properties_inside_tag[name.text()] = ''
                        else:
                            newitem = QTableWidgetItem()
                            newitem.setText(element.properties_inside_tag['id'])
                            self.ptable.setItem(i, 1, newitem)
            self.automated_activity = False

    def add_element(self, element: type[Element]):
        new_element = element()
        new_element.properties_inside_tag['id'] = f'{element.kind[1:-1]}-{len(self.elements)}'
        self.lookup[f'{element.kind[1:-1]}-{len(self.elements)}'] = new_element
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
                self.last_good_title = self.html.title()
                element = self.lookup[self.html.title()]
                self.ptable.setRowCount(len(element.properties_inside_tag.keys()))
                line = 0
                self.automated_activity = True
                for i in element.properties_inside_tag.keys():
                        self.ename.setText(self.html.title())
                        newitem = QTableWidgetItem()
                        newitem.setText(i)
                        self.ptable.setItem(line, 0, newitem)

                        newitem = QTableWidgetItem()
                        newitem.setText(element.properties_inside_tag[i])
                        self.ptable.setItem(line, 1, newitem)
                        line += 1
        self.automated_activity = False

window = MainWindow()
window.show()
app.exec()