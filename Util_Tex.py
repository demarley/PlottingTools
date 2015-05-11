rowStretch = 1.3

def PrintTexHeader(texFileName):
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
  
def PrintTexTrailer(texFileName):
  texFile=open(texFileName, 'a')
  print >> texFile, ""
  print >> texFile, "\\end{document}"
  texFile.close()

def PrintTexCode(texFileName, code):
  texFile=open(texFileName, 'a')
  print >> texFile, code
  texFile.close()
