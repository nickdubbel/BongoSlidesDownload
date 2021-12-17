# BongoSlidesDownload
 Download the slides of the bongo presentation during the presentation


Execute the program in the terminal.
Python BongoSlides.py [slide website without last number] [FileName.pdf]

To get the slides website:
1. Go tot the bongo lecture
2. Go to the browser developer tools (chrome f12)
3. Go to the network tab
4. Wait for the teacher to go to the next slide
5. Click in the slide number that appears
6. Copy the link and remove the last numbers until the /


imports:
os
sys
requests

#to create PDF from SVG files
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg

#to combine pdf's
from PyPDF2 import PdfFileMerger, PdfFileReader