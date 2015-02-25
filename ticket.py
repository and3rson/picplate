import xml.etree.ElementTree as ET
from PIL import Image, ImageColor, ImageDraw, ImageFont
import urllib
from StringIO import StringIO
import re

class TicketException(Exception): pass

class Ticket(object):
    def __init__(self, filename=None, xml=None, width=400, height=400):
        self.source = None

        if filename:
            self.load_file(filename)
        elif xml:
            self.load_xml(xml)

        self.context = {}
        self.width = width
        self.height = height

    def load_file(self, filename):
        self.source = ET.parse(filename)

    def load_xml(self, xml):
        self.source = ET.fromstring(xml)

    def assign(self, **kwargs):
        self.context.update(kwargs)

    def _compute_size(self, value, parent_value):
        if value.endswith('%'):
            return int(round(float(value.strip('%')) / 100 * parent_value))
        elif value.endswith('px'):
            return int(value.strip('px'))
        else:
            raise TicketException('Wrong dimension value: "{}"'.format(value))

    def render_element(self, element, parent=None):
        self.i += 1

        defaults = {
            'top': 0,
            'left': 0,
            'width': self.img.size[0],
            'height': self.img.size[1],
            'font-size': 12,
            'font-family': 'arial.pil',
            'background-color': None,
            'color': '#000000',
            'background-size': 'stretch',
            'background-image': None
        }

        if parent is None:
            # This is root element
            parent_computed = dict(defaults.items())
        else:
            parent_computed = parent.computed

        computed = {}

        no_inherit = ('background-color', 'background-size', 'background-image')

        for key in parent_computed.keys():
            value = element.attrib.get(key)

            if value is None:
                if key in no_inherit:
                    # Not inheriting, set default
                    computed[key] = defaults[key]
                else:
                    # Can be inherited
                    computed[key] = parent_computed[key]
            else:
                if key in ('left', 'top', 'width', 'height', 'font-size'):
                    if key in ('left', 'width'):
                        parent_value = parent_computed['width']
                    elif key in ('top', 'height', 'font-size'):
                        parent_value = parent_computed['height']
                    computed[key] = self._compute_size(value, parent_value)
                else:
                    computed[key] = value

                if key in ('top', 'left'):
                    computed[key] += parent_computed[key]

        element.computed = computed

        # Draw background (if set)
        if not (computed['background-color'] is None):
            self.draw.rectangle(((computed['left'], computed['top']), (computed['left'] + computed['width'], computed['top'] + computed['height'])), fill=ImageColor.getrgb(computed['background-color']))

        # Draw image (if set)
        if not (computed['background-image'] is None):
            url = computed['background-image']
            if url.startswith('http://') or url.startswith('https://'):
                raw = urllib.urlopen(url).read()
                img = Image.open(StringIO(raw))
                if computed['background-size'] == 'stretch':
                    img = img.resize((computed['width'], computed['height']), Image.BICUBIC)
                elif computed['background-size'] in ('cover', 'fit'):
                    bw = float(computed['width'])
                    bh = float(computed['height'])
                    iw = float(img.size[0])
                    ih = float(img.size[1])
                    xs = iw / bw
                    ys = ih / bh

                    if computed['background-size'] == 'cover':
                        if xs < ys:
                            dim = int(iw / xs), int(ih / xs)
                        else:
                            dim = int(iw / ys), int(ih / ys)
                    elif computed['background-size'] == 'fit':
                        if xs > ys:
                            dim = int(iw / xs), int(ih / xs)
                        else:
                            dim = int(iw / ys), int(ih / ys)
                    img = img.resize(dim, Image.BICUBIC)

                    xd, yd = int(img.size[0] - bw), int(img.size[1] - bh)

                    img = img.crop((xd / 2, yd / 2, img.size[0] - xd / 2, img.size[1] - yd / 2))
                else:
                    raise TicketException('Unknown background-size - "{}"'.format(computed['background-size']))

                if img.mode == 'RGBA':
                    self.img.paste(img, (computed['left'], computed['top']), img)
                else:
                    self.img.paste(img, (computed['left'], computed['top']))
            else:
                raise TicketException('Local images not yet implemented.')

        # Draw text (if set)
        text = element.text
        if not (text is None):
            text = text.strip()
            if len(text):
                lines = text.split('\n')
                font = ImageFont.truetype(computed['font-family'], computed['font-size'])
                offset = 0
                for line in lines:
                    line = line.strip()
                    for key, value in self.context.items():
                        line = re.sub('\{\{\s*(\w+)\s*\}\}', self._subst, line)
                    self.draw.text((computed['left'], computed['top'] + offset), line, font=font, fill=computed['color'])
                    offset += computed['font-size']

        for child in element:
            # Draw children
            self.render_element(child, element)

    def _subst(self, match):
        return self.context.get(match.group(1), '')

    def render(self, width=None, height=None):
        if width:
            self.width = width
        if height:
            self.height = height

        self.img = Image.new('RGBA', (self.width, self.height), color=ImageColor.getrgb('#FFFFFF'))
        self.draw = ImageDraw.Draw(self.img)

        self.i = 0
        self.render_element(self.source.getroot())

        return self.img