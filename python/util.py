"""
7 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Utilities for the plotting scripts.

Two classes: 
- html (writing html files)
- tex  (writing tex files)
"""


class HTML(object):
    """Functions for printing data to html files"""
    def PrintHtmlHeader(self,htmlFileName):

        htmlFile=open(htmlFileName, 'w')
        print >> htmlFile, "<!DOCTYPE html>"
        print >> htmlFile, "<html>"
        print >> htmlFile, "<body>"
        htmlFile.close()

        return


    def PrintHtmlTrailer(self,htmlFileName):

        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, "</body>"
        print >> htmlFile, "</html>"
        htmlFile.close()

        return


    def PrintHtmlCode(self,htmlFileName, code):

        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, code
        htmlFile.close()

        return

## END html


class TeX(object):
    """Functions for writing LaTeX"""
    def __init__(self):
        self.rowStretch = 1.3


    def PrintTexHeader(self,texFileName):

        texFile=open(texFileName, 'w')
        print >> texFile, "\\documentclass[letterpaper]{article}"
        print >> texFile, "\\usepackage{rotating}"
        print >> texFile, "\\usepackage{amsmath}"
        print >> texFile, "\\usepackage{amssymb}"
        print >> texFile, "\\usepackage{amsfonts}"
        print >> texFile, "\\usepackage{amsthm}"
        print >> texFile, "\\usepackage{graphicx}"
        print >> texFile, "\\usepackage{multirow}"
        print >> texFile, "\\usepackage{setspace}"
        print >> texFile, "\\usepackage{lscape}"
        print >> texFile, "\\usepackage{times}"
        print >> texFile, "\\usepackage{caption}"
        print >> texFile, "\\usepackage{cprotect}"
        print >> texFile, "\\renewcommand\\arraystretch{%s}" % rowStretch
        print >> texFile, "\\begin{document}"
        print >> texFile, ""
        texFile.close()

        return
  

    def PrintTexTrailer(self,texFileName):

        texFile=open(texFileName, 'a')
        print >> texFile, ""
        print >> texFile, "\\end{document}"
        texFile.close()

        return


    def PrintTexCode(self,texFileName, code):

        texFile=open(texFileName, 'a')
        print >> texFile, code
        texFile.close()

        return


## THE END ##