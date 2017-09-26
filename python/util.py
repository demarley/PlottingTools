"""
14 September 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Utilities for the plotting scripts.

Three classes: 
- html    (writing html files)
- tex     (writing tex files)
- verbose (printing output to terminal)
"""


class HTML(object):
    """Functions for printing data to html files"""
    def PrintHtmlHeader(self,htmlFileName):

        htmlFile = open(htmlFileName, 'w')
        print >> htmlFile, "<!DOCTYPE html>"
        print >> htmlFile, "<html>"
        print >> htmlFile, "<body>"
        htmlFile.close()

        return


    def PrintHtmlTrailer(self,htmlFileName):

        htmlFile = open(htmlFileName, 'a')
        print >> htmlFile, "</body>"
        print >> htmlFile, "</html>"
        htmlFile.close()

        return


    def PrintHtmlCode(self,htmlFileName, code):

        htmlFile = open(htmlFileName, 'a')
        print >> htmlFile, code
        htmlFile.close()

        return

## END html


class TeX(object):
    """Functions for writing LaTeX"""
    def __init__(self):
        self.rowStretch = 1.3


    def PrintTexHeader(self,texFileName):
        """Header to TeX file"""
        texFile = open(texFileName, 'w')
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
        """Trailer to TeX file"""
        texFile = open(texFileName, 'a')
        print >> texFile, ""
        print >> texFile, "\\end{document}"
        texFile.close()

        return


    def PrintTexCode(self,texFileName, code):
        """Write code to tex file"""
        texFile = open(texFileName, 'a')
        print >> texFile, code
        texFile.close()

        return
## End TeX


class VERBOSE(object):
    """
        Object for handling output to terminal.
        Same class in MuonAlignment repo

        @description Multiple "levels" for verbose output.
                     The higher the level, the less output is printed.
                     New level "MUTE" will silence all outputs.
    """
    def __init__(self,level="INFO"):
        self.verboseMap = {"DEBUG":  0,
                           "INFO":   1,
                           "WARNING":2,
                           "ERROR":  3,
                           "MUTE":   4};
        self.level = level
        self.name  = None

    def DEBUG(self,message):
        """Debug level - most verbose"""
        self.verbose("DEBUG",message)
        return

    def INFO(self,message):
        """Info level - standard output"""
        self.verbose("INFO",message)
        return

    def WARNING(self,message):
        """Warning level - if something seems wrong but code can continue"""
        self.verbose("WARNING",message)
        return

    def ERROR(self,message):
        """Error level - something is wrong"""
        self.verbose("ERROR",message)
        return

    def verbose(self,level,message):
        if self.verboseMap[level] >= self.verboseMap[self.level]:
            msg = "{0} : {1}".format(self.name,message) if self.name is not None else message
            print " {0} :: {1}".format(level,msg)

        return


## THE END ##