from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, \
QLabel, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QPlainTextEdit, QGridLayout, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
from python_elements import *
from functools import partial

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('ASimpleWYSIWYGEditor')

        self.body = Sbody()
        self.lookup: dict[str, Element] = {'pagebody-0': self.body}
        self.last_good_title = 'pagebody-0'
        self.automated_activity = False
        self.counter = 1

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
        addview.setFixedWidth(245)
        addview.setWidget(addcontainer)
        toolbox.addWidget(addview)

        mainbox.addWidget(toolcontainer)

        middlebox = QVBoxLayout()
        middlecontainer = QWidget()
        middlecontainer.setLayout(middlebox)

        html = QWebEngineView()
        html.titleChanged.connect(self.element_clicked)
        html.setZoomFactor(0.5)
        html.setFixedSize(QSize(960, 540))
        self.html = html
        self.refresh_html_content()
        middlebox.addWidget(html)

        childparentbox = QHBoxLayout()
        childparentcontainer = QWidget()
        childparentcontainer.setLayout(childparentbox)

        childview = QScrollArea()
        childbox = QGridLayout()
        childbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.childbox = childbox
        self.childwidgets: list[QPushButton] = []
        childcontainer = QWidget()
        childcontainer.setLayout(childbox)

        mainelement = QVBoxLayout()
        mainelementcontainer = QWidget()
        mainelementcontainer.setLayout(mainelement)
        mainelementcontainer.setFixedWidth(200)

        cname = QLabel()
        cname.setText('Select an element')
        font = cname.font()
        font.setPixelSize(18)
        cname.setFont(font)
        self.cname = cname
        mainelement.addWidget(cname)

        toparent = QPushButton()
        toparent.setText('Go to parent')
        toparent.clicked.connect(self.go_to_parent)
        mainelement.addWidget(toparent)

        updown = QHBoxLayout()
        updown.setContentsMargins(0, 0, 0, 0)
        updowncontainer = QWidget()
        updowncontainer.setLayout(updown)

        upbtn = QPushButton()
        upbtn.setText('Move up')
        upbtn.clicked.connect(self.move_up)
        dwbtn = QPushButton()
        dwbtn.setText('Move down')
        dwbtn.clicked.connect(self.move_down)
        updown.addWidget(upbtn)
        updown.addWidget(dwbtn)

        mainelement.addWidget(updowncontainer)

        delbtn = QPushButton()
        delbtn.setText('Delete element')
        delbtn.setStyleSheet('color: red;')
        delbtn.clicked.connect(self.delete_element)
        mainelement.addWidget(delbtn)

        childparentbox.addWidget(mainelementcontainer)

        childparentbox.addWidget(childcontainer)
        childview.setWidget(childparentcontainer)
        childview.setWidgetResizable(True)
        childview.setFixedSize(QSize(960, 180))

        middlebox.addWidget(childview)

        mainbox.addWidget(middlecontainer)

        properties_container = QWidget()
        properties = QVBoxLayout()
        properties.setAlignment(Qt.AlignmentFlag.AlignTop)
        properties_container.setLayout(properties)

        pcsstitle = QLabel()
        pcsstitle.setText('CSS properties')
        font = pcsstitle.font()
        font.setPixelSize(18)
        font.setBold(True)
        pcsstitle.setFont(font)
        properties.addWidget(pcsstitle)

        pcssinput = QPlainTextEdit()
        pcssinput.textChanged.connect(self.update_css)
        pcssinput.setStyleSheet('border-style: solid; border-width: 1px;')
        self.pcss = pcssinput
        properties.addWidget(pcssinput)

        ptitle = QLabel()
        font = self.font()
        font.setPixelSize(18)
        font.setBold(True)
        ptitle.setFont(font)
        ptitle.setText('Element properties')
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
        ptable.setFixedWidth(227)
        ptable.setFixedHeight(150)
        ptable.setRowCount(1)
        ptable.setColumnCount(2)
        ptable.setHorizontalHeaderLabels(['name', 'value'])
        ptable.cellChanged.connect(self.update_tag_properties)
        self.ptable = ptable
        properties.addWidget(ptable)

        export = QPushButton()
        export.setText('Export HTML document')
        export.clicked.connect(self.export_html)
        properties.addWidget(export)

        mainbox.addWidget(properties_container)

        self.setCentralWidget(maincontainer)

    def export_html(self):
        f = open('template.html')
        r = f.read()
        top_top = r[:r.index('/*stylearea*/')]
        top_middle = ''
        top_bottom = r[r.index('/*stylearea*/')+len('/*stylearea*/'):r.index('<!--addarea%-->')]
        bottom = r[r.index('<!--addarea%-->')+len('<!--addarea%-->'):]
        f.close()
        middle = ''
        self.body.properties_inside_tag.pop('onload')
        ihtml, (icss, iccss) = self.body.to_html(), self.body.get_css()
        self.body.properties_inside_tag['onload'] = 'loaded()'
        middle += ihtml + '\n'
        top_middle += f'#{self.body.properties_inside_tag['id']} {{\n'
        top_middle += icss
        top_middle += '\n}\n'
        top_middle += iccss

        top = top_top + top_middle + top_bottom
        total = top + middle + bottom
        filedialog = QFileDialog()
        name, _ = filedialog.getSaveFileName(self, 'Export HTML document', filter="HTML document (*.html)")
        if name:
            if not name.endswith('.html'):
                name += '.html'
            f = open(name, 'w')
            f.write(total)
            f.close()

    def move_up(self):
        element = self.lookup[self.last_good_title]
        if Element in type(element.parent).mro():
            parent: Element = element.parent #type: ignore
            index = parent.contains.index(element)
            if index > 0:
                parent.contains[index-1], parent.contains[index] = parent.contains[index], parent.contains[index-1]
        self.refresh_html_content()

    def move_down(self):
            element = self.lookup[self.last_good_title]
            if Element in type(element.parent).mro():
                parent: Element = element.parent #type: ignore
                index = parent.contains.index(element)
                if index < len(parent.contains)-1:
                    parent.contains[index+1], parent.contains[index] = parent.contains[index], parent.contains[index+1]
            self.refresh_html_content()

    def delete_element(self):
        element = self.lookup[self.last_good_title]
        if type(Element) != Sbody and Element in type(element.parent).mro():
            element.parent.contains.remove(element) #type: ignore
            self.child_clicked(element.parent.properties_inside_tag['id']) #type: ignore
            del element
            self.refresh_html_content()

    def go_to_parent(self):
        element = self.lookup[self.last_good_title]
        if Element in type(element.parent).mro():
            self.child_clicked(element.parent.properties_inside_tag['id']) #type: ignore
            
    def print_tree(self, element: Element, levels: int = 1):
        for i in element.contains:
            print('  '*levels, i.properties_inside_tag['id'])
            self.print_tree(i, levels+1)

    def add_row(self):
        self.ptable.setRowCount(self.ptable.rowCount()+1)

    def update_tag_properties(self):
        if not self.automated_activity:
            if self.last_good_title != None:
                self.automated_activity = True
                element = self.lookup[self.last_good_title]

                _id = element.properties_inside_tag['id']
                element.properties_inside_tag.clear()
                element.properties_inside_tag['id'] = _id
                refresh = False
                for i in range(self.ptable.rowCount()):
                    name = self.ptable.item(i, 0)
                    value = self.ptable.item(i, 1)
                    if type(name) == QTableWidgetItem and type(value) == QTableWidgetItem:
                        if name.text() != 'id':
                            if name.text() != '':
                                    element.properties_inside_tag[name.text()] = value.text()
                                    refresh = True
                            else:
                                self.ptable.removeRow(i)
                                refresh = True
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
                if Sbody in type(element).mro():
                    self.body.properties_inside_tag['onload'] = 'loaded()'
                    self.child_clicked('pagebody-0')
                if refresh:
                    self.refresh_html_content()
            self.automated_activity = False
    
    def update_css(self):
        if not self.automated_activity:
            if self.last_good_title != None:
                element = self.lookup[self.last_good_title]
                prev = element.css
                element.css = self.pcss.toPlainText()
                if element.is_my_css_valid():
                    self.refresh_html_content()
                    self.pcss.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')
                else:
                    element.css = prev
                    self.pcss.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')

    def add_element(self, element: type[Element]):
        parent = self.lookup[self.last_good_title]
        new_element = element(parent)
        new_element.properties_inside_tag['id'] = f'{element.kind[1:-1]}-{self.counter}'
        self.lookup[f'{element.kind[1:-1]}-{self.counter}'] = new_element
        parent.contains.append(new_element)
        self.counter += 1
        ids = []
        for child in new_element.contains:
            ids.append(child.kind[1:-1]+'-'+str(len(self.lookup.keys())))
            self.lookup[child.kind[1:-1]+'-'+str(len(self.lookup.keys()))] = child
            self.counter += 1
        new_element.give_out_ids(ids)
        self.refresh_html_content()
        self.child_clicked(self.last_good_title)

    def refresh_html_content(self):
        f = open('translator.html')
        r = f.read()
        top_top = r[:r.index('/*stylearea*/')]
        top_middle = ''
        top_bottom = r[r.index('/*stylearea*/')+len('/*stylearea*/'):r.index('<!--addarea%-->')]
        bottom = r[r.index('<!--addarea%-->')+len('<!--addarea%-->'):]
        f.close()
        middle = ''
        ihtml, (icss, iccss) = self.body.to_html(), self.body.get_css()
        middle += ihtml + '\n'
        top_middle += f'#{self.body.properties_inside_tag['id']} {{\n'
        top_middle += icss
        top_middle += '\n}\n'
        top_middle += iccss

        top = top_top + top_middle + top_bottom
        self.html.setHtml(top + middle + bottom)

    def child_clicked(self, id: str):
        self.last_good_title = id
        element = self.lookup[id]
        self.ptable.setRowCount(len(element.properties_inside_tag.keys()))
        line = 0
        self.automated_activity = True
        self.ename.setText(id)
        self.cname.setText(id)
        for i in element.properties_inside_tag.keys():
                newitem = QTableWidgetItem()
                newitem.setText(i)
                self.ptable.setItem(line, 0, newitem)

                newitem = QTableWidgetItem()
                newitem.setText(element.properties_inside_tag[i])
                self.ptable.setItem(line, 1, newitem)
                line += 1
        self.pcss.setPlainText(element.css)
        for button in self.childwidgets:
            self.childbox.removeWidget(button)
            button.deleteLater()
        self.childwidgets.clear()
        kinds: dict[str, int] = {}
        index = 0
        for child in element.contains:
            cbtn = QPushButton()
            if child.kind not in kinds.keys():
                cbtn.setText(child.friendly_name + ' [1]')
                kinds[child.kind] = 2
            else:
                cbtn.setText(f'{child.friendly_name} [{kinds[child.kind]}]')
                kinds[child.kind] += 1
            cbtn.clicked.connect(partial(self.child_clicked, child.properties_inside_tag['id']))
            self.childbox.addWidget(cbtn, index%4, index//4)
            self.childwidgets.append(cbtn)
            index += 1
        self.automated_activity = False

    def element_clicked(self):
        if self.html.title() != 'default-title' and self.html.title() != 'about:blank' and len(self.html.title()) < 40:
            if self.html.title() not in self.lookup:
                self.html.back()
                self.refresh_html_content()
            else:
                self.last_good_title = self.html.title()
                element = self.lookup[self.html.title()]
                self.ptable.setRowCount(len(element.properties_inside_tag.keys()))
                line = 0
                self.automated_activity = True
                self.ename.setText(self.html.title())
                self.cname.setText(self.html.title())
                for i in element.properties_inside_tag.keys():
                        newitem = QTableWidgetItem()
                        newitem.setText(i)
                        self.ptable.setItem(line, 0, newitem)
                        newitem = QTableWidgetItem()
                        newitem.setText(element.properties_inside_tag[i])
                        self.ptable.setItem(line, 1, newitem)
                        line += 1
                self.pcss.setPlainText(element.css)
                for button in self.childwidgets:
                    self.childbox.removeWidget(button)
                    button.deleteLater()
                    self.childwidgets.remove(button)
                kinds: dict[str, int] = {}
                index = 0
                for child in element.contains:
                    cbtn = QPushButton()
                    if child.kind not in kinds.keys():
                        cbtn.setText(child.friendly_name + ' [1]')
                        kinds[child.kind] = 2
                    else:
                        cbtn.setText(f'{child.friendly_name} [{kinds[child.kind]}]')
                        kinds[child.kind] += 1
                    cbtn.clicked.connect(partial(self.child_clicked, child.properties_inside_tag['id']))
                    self.childbox.addWidget(cbtn, index%4, index//4)
                    self.childwidgets.append(cbtn)
                    index += 1
        self.automated_activity = False

window = MainWindow()
window.show()
app.exec()