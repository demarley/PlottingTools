"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Write output to tables.
"""
from util import HTML,TeX

class Table:
    """Class for writing detector information to TeX and html tables"""
    def __init__(self):
        self.data = []
        self.html = HTML()
        self.tex  = TeX()


    def PrintData(self):
        print self.data
        return


    def PrintHtml(self, htmlFileName, caption="Caption", isComplete=False):
        return


    def PrintTex(self, texFileName, caption="Caption", label="table", isComplete=False):
        return


    ## "Group Table" functions
    def GetVarName(self,varIndex):
        return self.data[varIndex][0][0]


    def GetVarIndex(self, varName):
        for varIndex,d in enumerate( self.data ):
            if d[0][0] == varName:
                return varIndex
        print "ERROR :: TABLE : No such variable:", varName

        return -1


## THE END ##
