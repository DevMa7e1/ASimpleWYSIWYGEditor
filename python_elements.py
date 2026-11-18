class Element:
    kind = '<undefined>'
    properties_inside_tag = {'id': 'default'}
    contains: list[Element] = []

    def __init__(self) -> None:
        self.contains.clear()
        self.properties_inside_tag = {'id': 'default'}

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            pinside += f' {i}="{self.properties_inside_tag[i]}"'
        innerhtml = ''
        for element in self.contains:
            innerhtml += element.to_html()
        return self.kind[:-1] + pinside + '>' + innerhtml + '</' + self.kind[1:]

class Text(Element):
    kind = ''
    text = ''
    def to_html(self) -> str:
        return self.text

class Sh1(Element):
    kind = '<h1>'