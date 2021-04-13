#!/usr/bin/python3

from os import system
import sys
from typing import Tuple
from PyPDF2.generic import RectangleObject
from PyPDF2.pdf import PageObject
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from PyPDF2 import PdfFileReader, PdfFileWriter


file = sys.argv[1]

class PaperSize:
    h = 0
    w = 0
    def __init__(self, w: float, h: float):
        self.h = h
        self.w = w
def applyTransform():
    r = RectangleObject([0,0])
    x, y = r.lowerLeft
def transform(s: float, rotate: bool, tx: float, ty: float) -> Tuple:
    if rotate:
        return (0, -s, s, 0, tx, ty)
    else:
        return (s, 0, 0, s, tx, ty)
class Main(QWidget):

    size_letter = PaperSize(612,792)
    size_a4 = PaperSize(595.28,841.89)
    opt_bnw = True
    opt_n_per_page = 1
    opt_potrait = True
    opt_both_sides = True
    # 0 - A4
    # 1 - Letter
    opt_paper = 0

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignTop)

        colorRow = QHBoxLayout()
        colorMenu = QComboBox()
        colorMenu.addItem("Black and White")
        colorMenu.addItem("CMYK")
        colorMenu.activated.connect(self.changeColor)
        colorRow.addWidget(QLabel("Color"))
        colorRow.addWidget(colorMenu)
        vbox.addLayout(colorRow)

        paperRow = QHBoxLayout()
        paperMenu = QComboBox()
        paperMenu.addItem("A4")
        paperMenu.addItem("Letter")
        paperMenu.activated.connect(self.changePaper)
        paperRow.addWidget(QLabel("Paper"))
        paperRow.addWidget(paperMenu)
        vbox.addLayout(paperRow)

        npRow = QHBoxLayout()
        npMenu = QComboBox()
        npMenu.addItem("1")
        npMenu.addItem("2")
        npMenu.addItem("4")
        npMenu.activated.connect(self.changeNP)
        npRow.addWidget(QLabel("Pages per side"))
        npRow.addWidget(npMenu)
        vbox.addLayout(npRow)

        orntRow = QHBoxLayout()
        orntMenu = QComboBox()
        orntMenu.addItem("Portrait")
        orntMenu.addItem("Landscape")
        orntMenu.activated.connect(self.changeOrnt)
        orntRow.addWidget(QLabel("Orientation"))
        orntRow.addWidget(orntMenu)
        vbox.addLayout(orntRow)

        bthsRow = QHBoxLayout()
        bthsMenu = QComboBox()
        bthsMenu.addItem("Yes")
        bthsMenu.addItem("No")
        bthsMenu.activated.connect(self.changeBths)
        bthsRow.addWidget(QLabel("Print on both sides"))
        bthsRow.addWidget(bthsMenu)
        vbox.addLayout(bthsRow)

        btnRow = QHBoxLayout()
        prntBtn = QPushButton("Print")
        prntBtn.clicked.connect(self.print)
        cnclBtn = QPushButton("Cancel")
        cnclBtn.clicked.connect(self.close)
        btnRow.addWidget(prntBtn)
        btnRow.addWidget(cnclBtn)
        vbox.addStretch(1)
        vbox.addLayout(btnRow)

        vbox.addWidget(QLabel(file))

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Custom Print')
        self.show()

    def closeEvent(self, event) -> None:
        system("lprm -") #clear print-queue before exiting
        system("rm __custom_print_temp_out_*.pdf")
        return super().closeEvent(event)

    def changeColor(self, index):
        self.opt_bnw = index == 0
    def changeNP(self, index):
        self.opt_n_per_page = index + 1 if index < 2 else 4
    def changePaper(self, index):
        self.opt_paper = index
    def changeOrnt(self, index):
        self.opt_potrait = index == 0
    def changeBths(self, index):
        self.opt_both_sides = index == 0

    def print(self):
        src = PdfFileReader(open(file,'rb'))
        dst = []
        dst.append(PdfFileWriter())
        if self.opt_both_sides:
            dst.append(PdfFileWriter())
        n = src.getNumPages()
        size = self.size_a4 if self.opt_paper == 0 else self.size_letter
        W = size.w
        H = size.h
        j = 0
        k = 0
        dst_page = None
        for i in range(n):
            src_page = src.getPage(i)
            if j == 0:
                dst_page = dst[k].addBlankPage(W, H)
                k = (k + 1)%2 if self.opt_both_sides else k
            h0 = float(src_page.mediaBox.getHeight())
            w0 = float(src_page.mediaBox.getWidth())
            if self.opt_n_per_page == 1:
                if self.opt_potrait:
                    R = 0
                    r1 = H/h0
                    r2 = W/w0
                else:
                    R = -90
                    r1 = H/w0
                    r2 = W/h0
                if r1 < r2:
                    r = r1
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = (W - w)/2
                    ty = 0 
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, tx, ty + dy)
                else:
                    r = r2
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = 0
                    ty = (H - h)/2
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, tx, ty + dy)
            elif self.opt_n_per_page == 2:
                if self.opt_potrait:
                    R = 0
                    r1 = H/h0/2
                    r2 = W/w0
                else:
                    R = -90
                    r1 = H/w0/2
                    r2 = W/h0
                if r1 < r2:
                    r = r1
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = (W - w)/2
                    ty = H/2
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, tx, ty*(1-j) + dy)
                else:
                    r = r2
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = 0
                    ty = (H/2 - h)/2
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, tx, ty + H*(1-j)/2 + dy)
                j = (j+1)%2
            elif self.opt_n_per_page == 4:
                if self.opt_potrait:
                    R = 0
                    r1 = H/h0/2
                    r2 = W/w0/2
                else:
                    R = -90
                    r1 = H/w0/2
                    r2 = W/h0/2
                if r1 < r2:
                    r = r1
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = (W/2 - w)/2
                    ty = H/2
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, tx + (int((j & 1)!=0)^int(R != 0))*W/2, int((j & 2)==0)*ty + dy)
                else:
                    r = r2
                    if self.opt_potrait:
                        h = r*h0
                        w = r*w0
                        dy = 0
                    else:
                        h = r*w0
                        w = r*h0
                        dy = h
                    tx = W/2
                    ty = (H/2 - h)/2
                    dst_page.mergeRotatedScaledTranslatedPage(src_page, R, r, (int((j & 1)!=0)^int(R != 0))*tx, ty + int((j & 2)==0)*H/2 + dy)
                j = (j+1)%4
        dst[0].write(open('__custom_print_temp_out_1.pdf', 'wb'))
        if self.opt_both_sides:
            n1 = dst[0].getNumPages()
            n2 = dst[1].getNumPages()
            if n1 > n2:
                for i in range(n1-n2):
                    dst[1].addBlankPage(W,H)
            dst[1].write(open('__custom_print_temp_out_2.pdf', 'wb'))
        system("lpoptions -o ColorModel=%s"%("Black" if self.opt_bnw else "CMYK"))
        system("lpoptions -o PageSize=%s"%("A4" if self.opt_paper == 0 else "Letter"))
        system("lprm -") #clear previous jobs
        system("lp __custom_print_temp_out_1.pdf")
        if self.opt_both_sides:
            msgBox = QMessageBox()
            msgBox.setText("The first side is being printed. If the printer hasn't started yet, please make sure it's connected.")
            msgBox.setInformativeText("Confirm if the first side completes. Do you want to start printing the other side?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Yes)
            ret = msgBox.exec_()
            if ret == QMessageBox.Yes:
                system("lp __custom_print_temp_out_2.pdf")
def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
