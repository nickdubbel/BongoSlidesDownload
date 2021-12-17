import os
import sys
import requests

#to create PDF from SVG files
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg

#to combine pdf's
from PyPDF2 import PdfFileMerger, PdfFileReader



#settings
outputFileNameStandard = "BongoSlides.pdf"
#url = 'https://vc-bongo-eu-34-243-38-42.youseeu.com/bigbluebutton/presentation/75e51d4aae6f837a62eb59dfe503feab600b02fd-1638524141067/75e51d4aae6f837a62eb59dfe503feab600b02fd-1638524141067/d2d9a672040fbde2a47a10bf6c37b6a4b5ae187f-1638524141077/svg/'
#      https://vc-bongo-eu-34-243-38-42.youseeu.com/html5client/join?sessionToken=kvell8wrd5rekr7b
standardUrl = "https://vc-bongo-eu-176-34-66-91.youseeu.com/bigbluebutton/presentation/7094c4f4705ebeca9fe127d17b4b32c141c31d18-1638776007202/7094c4f4705ebeca9fe127d17b4b32c141c31d18-1638776007202/f63d2d3db2da61e1467b6d1b84d60d0460977fca-1638776096251/svg/"
standardUrl = ""

notfound = '<html>\r\n<head><title>404 Not Found</title></head>\r\n<body bgcolor="white">\r\n<center><h1>404 Not Found</h1></center>\r\n<hr><center>nginx/1.10.3 (Ubuntu)</center>\r\n</body>\r\n</html>\r\n'
dirName = 'files'






def svg_demo(image_path, output_path):
    drawing = svg2rlg(image_path)
    renderPDF.drawToFile(drawing, output_path)
    #renderPM.drawToFile(drawing, 'svg_demo.png', 'PNG')

def MergePDF(amountOfPDF, _outputFileName):

    print('merging files')

    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()
    
    # I had 116 files in the folder that had to be merged into a single document
    # Loop through all of them and append their pages
    for fileNumber in range(1, amountOfPDF):
        mergedObject.append(PdfFileReader(dirName+'/file' + str(fileNumber)+ '.pdf', 'rb'))
        os.remove(dirName+'/file' + str(fileNumber)+ '.pdf')
    
    # Write all the files into a file which is named as shown below
    mergedObject.write(_outputFileName)
    os.rmdir(dirName)
    

def main():

    # Check for the command line input
    if len(sys.argv) > 1:
        url = sys.argv[1]  
    else:
        url = standardUrl      

    if len(sys.argv) > 2:
        outputFileName = sys.argv[2]
    else:
        outputFileName = outputFileNameStandard

        
    
    # Create temp target Directory
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
        print("Remove this folder by hand")
        exit()

    #check for al the slides
    i = 1
    while i < 500:
        print (i)
        slideURL = url + str(i)

        #retrieve the slide from the internet
        try:
            r = requests.get(slideURL, allow_redirects=True)
        except:
            if i == 1:
                print('Website can not be reached')
                exit()
            else:
                print('ERROR, probably not all files included')
                MergePDF(i, outputFileName)
                print('created pdf with not all slides')
                exit()


        #if the slide is not retrievable (or the session is over, or we have past the last slide)
        if(r.text == notfound):
            if i == 1:
                print('slides not found (is the session over?)')
                os.rmdir(dirName)
                exit()
            else:
                #we have passed the last slide
                #Combnie all the pdf files into 1
                MergePDF(i, outputFileName)
                print("Download succesfull")
                exit()

        #save as SVG, convert to PDF, remove the old SVG
        svgLocation = 'files/file'+str(i)+'.svg'
        open(svgLocation, 'wb').write(r.content)
        svg_demo(svgLocation, 'files/file'+str(i)+'.pdf')
        os.remove(svgLocation)
        print(r)
        i += 1
    print('over the limit of 500 slides')
    print('this limit can be upgraded in the code')



if __name__ == "__main__":
    main()
