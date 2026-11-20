from _collections_abc import dict_keys
from typing import Any

class Element:
    kind = '<undefined>'
    friendly_name = 'Undefined element'

    def __init__(self) -> None:
        self.contains: list[Element] = []
        self.properties_inside_tag = {'id': 'default'}
        self.css = ''
        self.set_default()

    def set_default(self) -> None:
        pass

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            pinside += f' {i}="{self.properties_inside_tag[i]}"'
        innerhtml = ''
        for element in self.contains:
            innerhtml += element.to_html()
        return self.kind[:-1] + pinside + '>' + innerhtml + '</' + self.kind[1:]

    def get_css(self) -> tuple[str, str]:
        ccss = ''
        for element in self.contains:
            ccss += f'#{element.properties_inside_tag['id']} {{\n'
            selfcss, childcss = element.get_css()
            ccss += selfcss
            ccss += '\n}\n'
            ccss += childcss
        return self.css, ccss
    def is_my_css_valid(self):
        valid = True
        for line in self.css.split('\n'):
            if line.count(':') < 1:
                valid = False
                break
        if valid:
            if len(self.css.split('\n')) > 1:
                if not self.css.split('\n')[-2].endswith(';'):
                    valid = False
        return valid

class Text(Element):
    kind = ''
    text = ''

    class text_dict(dict):
        def set_owner(self, owner: Text):
            self.owner = owner
        def __setitem__(self, key: Any, value: Any) -> None:
            if key == 'text':
                self.owner.text = value
            else:
                super().__setitem__(key, value)
        def __getitem__(self, key: Any) -> Any:
            if key == 'text':
                return self.owner.text
            return super().__getitem__(key)
        def keys(self) -> list: #type: ignore
            return list(super().keys()) + ['text']
        def __len__(self) -> int:
            return super().__len__() + 1
    
    def __init__(self) -> None:
        super().__init__()
        self.properties_inside_tag = self.text_dict()
        self.properties_inside_tag.set_owner(self)
        self.properties_inside_tag['id'] = 'default'

    def set_default(self) -> None:
        self.text = 'Text element'
    def to_html(self) -> str:
        return self.text

# Text elements
class Sp(Element):
    kind = '<p>'
    friendly_name = 'Paragraph (<p>)'
    def set_default(self) -> None:
        self.contains.append(Text())
class Sh1(Sp):
    kind = '<h1>'
    friendly_name = 'Heading 1 (<h1>)'
class Sh2(Sp):
    kind = '<h2>'
    friendly_name = 'Heading 2 (<h2>)'
class Sh3(Sp):
    kind = '<h3>'
    friendly_name = 'Heading 3 (<h3>)'
class Sh4(Sp):
    kind = '<h4>'
    friendly_name = 'Heading 4 (<h4>)'
class Sh5(Sp):
    kind = '<h5>'
    friendly_name = 'Heading 5 (<h5>)'
class Sh6(Sp):
    kind = '<h6>'
    friendly_name = 'Heading 6 (<h6>)'

# General elements
class Sbutton(Element):
    kind = '<button>'
    friendly_name = 'Button (<button>)'
class Simg(Element):
    kind = '<img>'
    friendly_name = 'Image (<img>)'

    def set_default(self) -> None:
        self.properties_inside_tag['height'] = '100'
        self.properties_inside_tag['width'] = '100'

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            pinside += f' {i}="{self.properties_inside_tag[i]}"'
        return self.kind[:-1] + pinside + '>'

all_elements: dict[str, list[type[Element]]] = {'Text elements': [Sh1, Sh2, Sh3, Sh4, Sh5, Sh6, Sp], 'General elements': [Sbutton, Simg]}