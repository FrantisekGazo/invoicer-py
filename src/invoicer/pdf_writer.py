from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from model import *
import os


class Font(object):
    Regular = 'Regular'
    Bold = 'Bold'
    Light = 'Light'


class Gravity(object):
    CENTER = 1
    LEFT = 2
    RIGHT = 3


class PriceFormat(object):
    NONE = 0
    FRONT = 1
    BACK = 2


class PdfWriter(object):
    def __init__(self, resources, full_path, document):
        self.resources = resources

        pdfmetrics.registerFont(TTFont(Font.Regular, resources.get_font('Roboto-Regular')))
        pdfmetrics.registerFont(TTFont(Font.Bold, resources.get_font('Roboto-Bold')))
        pdfmetrics.registerFont(TTFont(Font.Light, resources.get_font('Roboto-Light')))

        pagesize = A4
        self._page_width, self._page_height = pagesize

        c = Canvas(full_path, pagesize=pagesize)
        c.setLineWidth(.3)
        self.canvas = c

        self._line_height = 0
        self._vertical_spacing = 5
        self._page_padding_horizontal = 60
        self._page_padding_vertical = 40
        self._default_font_size = 10
        self._default_font_name = Font.Regular
        self._change_font()

        self.document = document
        self._x = 0
        self._y = self._page_height

    def write(self):
        # header
        header_y = self._page_height - self._page_padding_vertical
        self._x = self._page_padding_horizontal
        self._y = header_y
        self._write_header()

        # contractor
        contractor_y = header_y - 30
        self._x = self._page_padding_horizontal
        self._y = contractor_y
        self._write_contractor()
        contractor_final_y = self._y

        # client
        self._x = self._page_width / 2
        self._y = contractor_y
        self._write_client(self._page_width / 2 - self._page_padding_horizontal)
        client_final_y = self._y

        # dates
        usable_width = self._page_width - 2 * self._page_padding_horizontal
        self._x = self._page_padding_horizontal
        self._y = min(contractor_final_y, client_final_y) - 10
        self._write_dates(usable_width)

        # bank account
        self._x = self._page_padding_horizontal
        self._y -= 0
        self._write_bank_account(usable_width)

        # items
        self._x = self._page_padding_horizontal
        self._y -= 20
        self._write_items(self._page_width - 2 * self._page_padding_horizontal)

        # sum
        self._x = self._page_width / 2 + 10
        self._y -= 0
        self._write_sum(self._page_width / 2 - 10 - self._page_padding_horizontal - 4)

        # signature
        self._x = self._page_width * 2 / 3
        self._y -= 20
        self._write_signature(width=100, height=60)

        self.canvas.save()

    def _write_header(self):
        original_x = self._x
        original_y = self._y

        self._change_font()
        self._write_formatted_string('document')

        self._x += 40
        self._y = original_y
        self._change_font(name=Font.Bold, size=12)
        self._write_string(self.document.number)

        self._x += original_x

    def _write_contractor(self):
        self._change_font(name=Font.Light)
        self._write_string(self.resources.get_string('contractor'))

        self._y -= 5
        self._change_font(name=Font.Bold)
        self._write_string(self.document.contractor.name)

        self._change_font()
        self._write_strings(self.document.contractor.address)

        self._y -= 5
        self._write_formatted_string('ico', self.document.contractor.ico)
        self._write_formatted_string('dic', self.document.contractor.dic)
        if self.document.client.is_foreign():
            self._write_formatted_string('icdph', self.document.contractor.icdph)
            self._change_font(size=8)
            self._write_formatted_string('dph_p7_1')
            self._write_formatted_string('dph_p7_2')
        else:
            self._change_font(size=8)
            self._write_formatted_string('dph_no')

        self._y -= 5
        self._change_font()
        self._write_formatted_string('phone', self.document.contractor.phone)
        self._write_formatted_string('email', self.document.contractor.email)

    def _write_client(self, width):
        original_y = self._y
        original_x = self._x

        # set left padding for lines
        self._x += 10

        self._y = original_y - self._line_height - 10
        self._change_font(name=Font.Bold)
        self._write_string(self.document.client.name)

        self._change_font()
        self._write_strings(self.document.client.address)

        self._y -= 10

        # frame
        height = original_y - self._y + self._line_height / 2 - 3
        self.canvas.roundRect(x=original_x - 10, y=self._y, width=width + 10, height=height, radius=5)
        self._y = original_y

        self._draw_image(self.resources.get_image('white'), x=self._x - 5, y=self._y, width=65, height=10)

        self._change_font(name=Font.Light)
        self._write_string(self.resources.get_string('client'))

        self._change_font()
        self._y -= (height + 5)
        self._write_formatted_string('ico', self.document.client.ico)
        self._write_formatted_string('dic', self.document.client.dic)
        self._write_formatted_string('icdph', self.document.client.icdph)

    def _write_dates(self, width):
        # line
        self._draw_line(self._x, self._y, self._x + width, self._y)

        y = self._y - 20

        self._x += 10
        self._y = y
        self._change_font()
        self._write_formatted_string('issue_date')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.issue_date)

        self._x += 100
        self._y = y
        self._change_font()
        self._write_formatted_string('delivery_date')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.delivery_date)

        self._x += 100
        self._y = y
        self._change_font()
        self._write_formatted_string('due_date')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.due_date)

    def _write_bank_account(self, width):
        padding = 20
        y = self._y - padding

        # frame
        height = self._line_height * 2 + padding
        self._draw_image(self.resources.get_image('gray'), x=self._x, y=self._y - height, width=width, height=height)
        self.canvas.rect(x=self._x, y=self._y - height, width=width, height=height)

        self._x += 10
        self._y = y
        self._change_font()
        self._write_formatted_string('iban')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.bank_account.iban)

        self._x += 200
        self._y = y
        self._change_font()
        self._write_formatted_string('swift')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.bank_account.swift)

        self._x += 90
        self._y = y
        self._change_font()
        self._write_formatted_string('variable_symbol')
        self._change_font(name=Font.Bold)
        self._write_string(self.document.number)

        self._x += 90
        self._y = y
        self._change_font()
        self._write_formatted_string('total_price')
        self._change_font(name=Font.Bold)
        self._write_formatted_price(self.document.total(), self.document.currency, format=PriceFormat.BACK)

    def _write_items(self, width):
        space = 5
        column_widths = [15, 200, 50, 35, 70, 76]
        column_starts = [0, 0, 0, 0, 0, 0]
        i = 1
        for column_width in column_widths:
            for c in range(i, len(column_widths)):
                column_starts[c] += column_width + space
            i += 1

        x = self._x
        y = self._y

        base_y = self._y - 4
        self._draw_image(self.resources.get_image('gray'), x=x, y=base_y, width=width, height=self._line_height + 4)
        self._draw_line(from_x=x, from_y=base_y, to_x=x + width, to_y=base_y)

        self._change_font(name=Font.Bold)
        self._x = x + column_starts[0] + column_widths[0]
        self._y = y
        self._write_formatted_string('item_number', gravity=Gravity.RIGHT)

        self._x = x + column_starts[1]
        self._y = y
        self._write_formatted_string('item_name')

        self._x = x + column_starts[2] + column_widths[2]
        self._y = y
        self._write_formatted_string('item_amount', gravity=Gravity.RIGHT)

        self._x = x + column_starts[3] + column_widths[3]
        self._y = y
        self._write_formatted_string('item_unit', gravity=Gravity.RIGHT)

        self._x = x + column_starts[4] + column_widths[4]
        self._y = y
        self._write_formatted_string('item_price', gravity=Gravity.RIGHT)

        self._x = x + column_starts[5] + column_widths[5]
        self._y = y
        self._write_formatted_string('item_total', gravity=Gravity.RIGHT)

        self._change_font()
        i = 0
        line_max_characters = 50
        extra_y = 0
        for item in self.document.items:
            i += 1
            y -= self._line_height + 3 + extra_y
            extra_y = 0

            self._x = x + column_starts[0] + column_widths[0]
            self._y = y
            self._write_string("%s." % i, gravity=Gravity.RIGHT)

            self._x = x + column_starts[1]
            self._y = y
            if len(item.name) > line_max_characters:
                rows = self.split_into_rows(item.name, line_max_characters)
                for row in rows:
                    self._write_string(row)
                    extra_y += self._line_height
                extra_y -= self._line_height
            else:
                self._write_string(item.name)

            self._x = x + column_starts[2] + column_widths[2]
            self._y = y
            self._write_formatted_price(item.amount, gravity=Gravity.RIGHT)

            self._x = x + column_starts[3] + column_widths[3]
            self._y = y
            self._write_string(item.unit, gravity=Gravity.RIGHT)

            self._x = x + column_starts[4] + column_widths[4]
            self._y = y
            self._write_formatted_price(item.price, gravity=Gravity.RIGHT)

            self._x = x + column_starts[5] + column_widths[5]
            self._y = y
            self._write_formatted_price(item.total(), gravity=Gravity.RIGHT)

            base_y -= self._line_height + 3 + extra_y
            self._draw_line(from_x=x, from_y=base_y, to_x=x + width, to_y=base_y)

    def _write_sum(self, width):
        x = self._x
        y = self._y - 30

        if self.document.discount > 0:
            self._change_font(name=Font.Bold, size=9)
            self._x = x
            self._y = y
            discount_percent = self._format_number(self.document.discount_percentage())
            self._write_formatted_string('discount', discount_percent)
            self._x += width
            self._y = y
            self._write_formatted_price(-self.document.discount, gravity=Gravity.RIGHT)

            y -= self._line_height

        self._change_font(name=Font.Bold)
        self._x = x
        self._y = y
        self._write_formatted_string('total')
        self._x += width
        self._y = y
        self._write_formatted_price(self.document.total(), self.document.currency,
                                    format=PriceFormat.FRONT, gravity=Gravity.RIGHT)

    def _write_signature(self, height, width):
        # line
        self._draw_image(self.document.contractor.signature, x=self._x, y=self._y - height, width=width, height=height,
                         preserve_aspect_ratio=True)
        self._draw_line(from_x=self._x, from_y=self._y - height, to_x=self._x + width, to_y=self._y - height)

        self._x += width / 2
        self._y -= height + 10
        self._change_font(size=8)
        self._write_formatted_string('signature', gravity=Gravity.CENTER)

    def _change_font(self, name=None, size=None):
        used_name = name if name is not None else self._default_font_name
        used_size = size if size is not None else self._default_font_size
        self._line_height = used_size + used_size * 0.25
        self.canvas.setFont(used_name, used_size)

    def _write_formatted_string(self, key, value=None, gravity=Gravity.LEFT):
        self._write_string(self.resources.get_string(key, value), gravity)

    def _write_string(self, line, gravity=Gravity.LEFT):
        if gravity == Gravity.CENTER:
            self.canvas.drawCentredString(self._x, self._y, line)
        elif gravity == Gravity.LEFT:
            self.canvas.drawString(self._x, self._y, line)
        else:
            self.canvas.drawRightString(self._x, self._y, line)
        self._y -= self._line_height

    def _write_strings(self, lines):
        for line in lines:
            self._write_string(line)

    def _draw_image(self, image_path, x, y, width=None, height=None, preserve_aspect_ratio=False):
        self.canvas.drawImage(image=image_path,
                              x=x, y=y, width=width, height=height,
                              preserveAspectRatio=preserve_aspect_ratio)

    def _draw_line(self, from_x, from_y, to_x, to_y):
        self.canvas.line(from_x, from_y, to_x, to_y)

    def _write_formatted_price(self, price, currency=Currency.NONE, format=PriceFormat.NONE, gravity=Gravity.LEFT):
        price = self._format_number(price)
        if format == PriceFormat.FRONT:
            self._write_string(currency.name + ' ' + price, gravity)
        elif format == PriceFormat.BACK:
            self._write_string(price + ' ' + currency.name, gravity)
        else:
            self._write_string(price, gravity)

    def _format_number(self, number):
        return "{:0,.2f}".format(number).replace(',', ' ').replace('.', ',')

    def split_into_rows(self, string, line_max_characters):
        rows = []

        words = string.split(' ')
        current_row = ''
        # buffer for prepositions
        temp = ''
        for word in words:
            if len(word) < 4:
                # if it is a preposition, store it in  buffer
                temp += word + ' '
            else:
                if len(current_row) + len(word) > line_max_characters:
                    rows.append(current_row)
                    current_row = ' '

                if len(temp) > 0:
                    current_row += temp
                    temp = ''

                current_row += word + ' '

        # make sure nothing was left in the buffer
        if len(temp) > 0:
            current_row += temp
        # add last row
        rows.append(current_row)

        return rows
