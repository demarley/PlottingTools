def PrintHtmlHeader(htmlFileName):
  htmlFile=open(htmlFileName, 'w')
  print >> htmlFile, "<!DOCTYPE html>"
  print >> htmlFile, "<html>"
  print >> htmlFile, "<body>"
  htmlFile.close()
  
def PrintHtmlTrailer(htmlFileName):
  htmlFile=open(htmlFileName, 'a')
  print >> htmlFile, "</body>"
  print >> htmlFile, "</html>"
  htmlFile.close()

def PrintHtmlCode(htmlFileName, code):
  htmlFile=open(htmlFileName, 'a')
  print >> htmlFile, code
  htmlFile.close()
