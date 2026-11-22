from typing import Any

class Element:
    kind = '<undefined>'
    friendly_name = 'Undefined element'

    def __init__(self, parent: Element | None = None) -> None:
        self.contains: list[Element] = []
        self.properties_inside_tag = {'id': 'default'}
        self.css = ''
        self.parent = parent
        self.set_default()

    def set_default(self) -> None:
        pass

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            if self.properties_inside_tag[i] != '':
                pinside += f' {i}="{self.properties_inside_tag[i]}"'
            else:
                pinside += f' {i}'
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
        if self.css == '':
            return True
        for line in self.css.split('\n'):
            if line.count(':') < 1:
                valid = False
                break
        if valid:
            if len(self.css.split('\n')) > 1:
                if not self.css.split('\n')[-2].endswith(';'):
                    valid = False
        return valid
    
    def give_out_ids(self, ids: list[str]):
        for i, id in enumerate(ids):
            self.contains[i].properties_inside_tag['id'] = id

# Internal elements
class Sbody(Element):
    kind = '<body>'
    friendly_name = 'Page body'
    def set_default(self) -> None:
        self.properties_inside_tag['id'] = 'pagebody-0'
class Text(Element):
    kind = '*text*'
    text = ''
    friendly_name = 'Text element'

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

    def set_default(self) -> None:
        self.properties_inside_tag = self.text_dict()
        self.properties_inside_tag.set_owner(self)
        self.properties_inside_tag['id'] = 'default'
        self.text = 'Text element'
    def to_html(self) -> str:
        return self.text

# Text elements
class Sp(Element):
    kind = '<p>'
    friendly_name = 'Paragraph (<p>)'
    def set_default(self) -> None:
        self.contains.append(Text(self))
class Sbr(Element):
    kind = '<br>'
    friendly_name = 'Line break (<br>)'
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
class Sabbr(Sp):
    kind = '<abbr>'
    friendly_name = 'Abbreviation (<abbr>)'
class Saddress(Sp):
    kind = '<address>'
    friendly_name = 'Contact address (<address>)'
class Sblockquote(Sp):
    kind = '<blockquote>'
    friendly_name = 'Block quotation (<blockquote>)'
class Scite(Sp):
    kind = '<cite>'
    friendly_name = 'Citation (<cite>)'
class Scode(Sp):
    kind = '<code>'
    friendly_name = 'Inline code (<code>)'
class Sins(Sp):
    kind = '<ins>'
    friendly_name = 'Inserted text (<ins>)'
class Sdel(Sp):
    kind = '<del>'
    friendly_name = 'Deleted text (<del>)'
class Sdetails(Sp):
    kind = '<details>'
    friendly_name = 'Details disclosure (<details>)'
class Skbd(Sp):
    kind = '<kbd>'
    friendly_name = 'Keyboard input (<kbd>)'
class Smark(Sp):
    kind = '<mark>'
    friendly_name = 'Mark text (<mark>)'
class Sq(Sp):
    kind = '<q>'
    friendly_name = 'Inline quotation (<q>)'
class Ssamp(Sp):
    kind = '<samp>'
    friendly_name = 'Sample output (<samp>)'
class Ssmall(Sp):
    kind = '<small>'
    friendly_name = 'Side comment (<small>)'
class Ssub(Sp):
    kind = '<sub>'
    friendly_name = 'Subscript (<sub>)'
class Ssup(Sp):
    kind = '<sup>'
    friendly_name = 'Superscript (<sup>)'
class Ssummary(Sp):
    kind = '<summary>'
    friendly_name = 'Disclosure summary (<summary>)'
class Svar(Sp):
    kind = '<var>'
    friendly_name = 'Variable (<var>)'

# Functional elements
class Sa(Sp):
    kind = '<a>'
    friendly_name = 'Anchor (<a>)'
class Sbutton(Sp):
    kind = '<button>'
    friendly_name = 'Button (<button>)'
class Sinput(Element):
    kind = '<input>'
    friendly_name = 'Input (<input>)'
class Stextarea(Element):
    kind = '<textarea>'
    friendly_name = 'Textarea (<textarea>)'
class Slabel(Sp):
    kind = '<label>'
    friendly_name = 'Item label (<label>)'
class Smeter(Element):
    kind = '<meter>'
    friendly_name = 'Meter (<meter>)'
class Sprogress(Element):
    kind = '<progress>'
    friendly_name = 'Progress indicator (<progress>)'
class Siframe(Element):
    kind = '<iframe>'
    friendly_name = 'Inline frame (<iframe>)'

# Media elements
class Simg(Element):
    kind = '<img>'
    friendly_name = 'Image (<img>)'

    def set_default(self) -> None:
        self.properties_inside_tag['height'] = '100'
        self.properties_inside_tag['width'] = '100'

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            if self.properties_inside_tag[i] != '':
                pinside += f' {i}="{self.properties_inside_tag[i]}"'
            else:
                pinside += f' {i}'
        return self.kind[:-1] + pinside + '>'
class Saudio(Element):
    kind = '<audio>'
    friendly_name = 'Audio (<audio>)'
class Svideo(Element):
    kind = '<video>'
    friendly_name = 'Video (<video>)'
class Sembed(Element):
    kind = '<embed>'
    friendly_name = 'Embed external content (<embed>)'

    def set_default(self) -> None:
        self.properties_inside_tag['height'] = '100'
        self.properties_inside_tag['width'] = '100'

    def to_html(self) -> str:
        pinside = ''
        for i in self.properties_inside_tag.keys():
            if self.properties_inside_tag[i] != '':
                pinside += f' {i}="{self.properties_inside_tag[i]}"'
            else:
                pinside += f' {i}'
        return self.kind[:-1] + pinside + '>'
class Sobject(Element):
    kind = '<object>'
    friendly_name = 'External object (<object>)'

    def set_default(self) -> None:
        self.properties_inside_tag['height'] = '100'
        self.properties_inside_tag['width'] = '100'

# Page structure elements
class Sdiv(Element):
    kind = '<div>'
    friendly_name = 'Content division (<div>)'
    def set_default(self) -> None:
        self.css = 'height: 100px;\nwidth: 100px;\nborder-style: solid;'
class Sspan(Element):
    kind = '<span>'
    friendly_name = 'Content span (<span>)'
    def set_default(self) -> None:
        self.css = 'height: 100px;\nwidth: 100px;\nborder-style: solid;'
class Shr(Element):
    kind = '<hr>'
    friendly_name = 'Horizontal rule (<hr>)'

all_elements: dict[str, list[type[Element]]] = {'Functional elements': [Sa, Sbutton, Sinput, Stextarea, Slabel, Smeter, Sprogress, Siframe], \
'Media elements': [Simg, Saudio, Sembed, Sobject], \
'Text elements': [Sh1, Sh2, Sh3, Sh4, Sh5, Sh6, Sp, Sabbr, Saddress, Scite, Scode, Sins, Sdel, \
Sdetails, Skbd, Smark, Sq, Ssamp, Ssmall, Ssub, Ssup, Ssummary, Svar], \
'Page structure': [Sdiv, Sspan, Shr]}