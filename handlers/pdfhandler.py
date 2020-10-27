# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# load system modules
import io
import re
import time
from datetime import date
from textwrap import wrap

# load internal modules
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from defines import paths


def validate_html_date(html_date):
    """
    Validates a date (yyyy-mm-dd) roughly
    (yes, it's not the greatest date validation ever)
    """
    if re.match(r"[\d][\d][\d][\d]-[\d]?[\d]-[\d]?[\d]", html_date):
        year, month, day = html_date.split("-")
        if not int(year) > 1500:
            return False
        if not int(month) < 12:
            return False
        if not day < 31:
            return False
    else:
        return False


def validate_print_date(html_date):
    """
    Validates a date for display on the frontend.
    This should be an exact match of dd.mm.yyyy
    """
    return re.match(r"[\d][\d].[\d][\d].[\d][\d][\d][\d]", html_date)


def check_start_date(check_date):
    day, month, year = check_date.split(".")
    tdate = ".".join([day, month])
    if tdate == "31.08":
        return "01.09." + year
    else:
        return check_date


def reformat_date(date):
    year, month, day = date.split("-")
    date = ".".join([day, month, year])
    return date


def get_a_date(type=""):
    if type == "html":
        return time.strftime("%Y-%m-%d")
    else:
        return time.strftime("%d.%m.%Y")


def get_date(kw, type, nr, year):
    kw = int(kw)
    nr = int(nr) - 1

    year = int(year) - 1
    year = int(time.strftime("%Y")) + year
    kw = (kw + nr) % 52
    start_date = date.fromisocalendar(year, kw, 1)
    end_date = date.fromisocalendar(year, kw, 5)

    if type == "server":
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

    return start_date, end_date


def get_kw_from_date(d):
    # date formatted as: yyyy-mm-dd
    year, month, day = d.split("-")
    dateobj = date(int(year), int(month), int(day))
    iso_date = dateobj.isocalendar()
    return iso_date[1]  # only kw


def draw(data, uinput, packet):
    LINE_DISTANCE = 30
    nr = int(uinput["nr"])
    nr -= 1
    kw = data["kw"]
    kw = int(kw)
    kw = (kw + nr) % 52
    fullname = uinput["surname"] + " " + uinput["name"]
    start_date = reformat_date(uinput["start_date"])
    start_date = check_start_date(start_date)

    end_date = reformat_date(uinput["end_date"])
    sign_date = reformat_date(uinput["sign_date"])

    c = canvas.Canvas(packet, pagesize=A4)

    c.drawString(313, 795, fullname)
    c.drawString(386, 778, uinput["unit"])
    c.drawString(231, 748, str(nr + 1))
    c.drawString(260, 748, start_date)
    c.drawString(365, 748, end_date)
    c.drawString(530, 748, uinput["year"])

    # Betrieblich
    height = 680
    bcontent = uinput["Bcontent"].split("\n")
    for cont in bcontent:
        t = c.beginText()
        bcontent = "\n".join(wrap(cont, 80))
        t.setTextOrigin(60, height)
        t.textLines(bcontent)
        c.drawText(t)
        height -= LINE_DISTANCE

    # Schulungen
    height = 515
    scontent = uinput["Scontent"].split("\n")
    for scont in scontent:
        st = c.beginText()
        scontent = "\n".join(wrap(scont, 80))
        st.setTextOrigin(60, height)
        st.textLines(scontent)
        c.drawText(st)
        height -= LINE_DISTANCE

    # Berufschule
    height = 302
    bscontent = uinput["BScontent"].split("\n")
    for bscont in bscontent:
        bt = c.beginText()
        bscontent = "\n".join(wrap(bscont, 80))
        bt.setTextOrigin(60, height)
        bt.textLines(bscontent)
        c.drawText(bt)
        height -= LINE_DISTANCE

    c.drawString(95, 148, sign_date)
    c.drawString(260, 148, sign_date)
    c.drawString(430, 148, sign_date)
    c.save()
    return packet


def compile(packet):
    new_pdf = PdfFileReader(packet)
    template = PdfFileReader(open(paths.PDF_TEMPLATE_PATH, "rb"))
    out = PdfFileWriter()
    page = template.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    out.addPage(page)
    # filename = "./tmp/" + str(time.strftime("%H-%M_%d%m%Y")) + ".pdf"  # for unique filenames
    filename = paths.TMP_PATH + "save.pdf"
    out_stream = open(filename, "wb")
    out.write(out_stream)
    out_stream.close()
    return filename


def create_many(content):
    pages = PdfFileWriter()
    data = {}
    uinput = {}
    for c in content:
        packet = io.BytesIO()
        template = PdfFileReader(open(paths.PDF_TEMPLATE_PATH, "rb"))
        template_page = template.getPage(0)
        uinput["name"] = c[1]
        uinput["surname"] = c[2]
        data["kw"] = c[3]  # only for old draw method, CHANGE THIS SOON!!
        uinput["nr"] = int(c[4]) - 1  # this is because the draw method increases the nr automatically
        uinput["year"] = str(c[5])
        uinput["unit"] = c[6]
        uinput["start_date"] = c[7]
        uinput["end_date"] = c[8]
        uinput["sign_date"] = c[9]
        uinput["Bcontent"] = c[10]
        uinput["Scontent"] = c[11]
        uinput["BScontent"] = c[12]
        packet = draw(data, uinput, packet)
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        template_page.mergePage(new_pdf.getPage(0))
        pages.addPage(template_page)
        del packet
        del template_page
        del new_pdf

    filename = paths.TMP_PATH + "save.pdf"
    out_stream = open(filename, "wb")
    pages.write(out_stream)
    return filename
