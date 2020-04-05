# test.py
import cv2 as cv
import barcode
import pyzbar.pyzbar as pyzbar

# A class with init method


class CaptureFrame:

    def __init__(self, EAN, Capture):
        """
        init method is a contructor
        init funksjonen tar 3 parameter
        self: er en peker og trenger ikke ingen verdi
        EAN: er barcode av typen code39
        Capture: Bilde/Video fra webkamera
        """
        self.EAN = EAN
        self.Capture = Capture

    def getFrame(self):
        """
        Tar en parameter
        Count: er en global variable av typen int og den øker med 1 hver gang programmet tar et nytt bildet
        Barcode: er en global variable av typen string og får barcode verdien når den lest av programmet
        """
        Count = 0
        Barcode = ''
        """
            While loopen:
            Sjekker om webkameraet er åpent for bruk
            Leser bildetramme
            Gjør bildet blur 
            Sjekker om barcoden er lest
            
            Hvis knappen "c" er tastet inn så programmet vil ta  bildet og lager barcode så lagrer begge 
            bildet lagres i filen "images"
            barcoden lagres i filen "barcodes"
            Programmet kjører ikke dersom webkamera er ikke koblet inn
        """
        while (True):
            if self.Capture.isOpened():
                Ret, Frame = self.Capture.read()
                BlurImage = cv.GaussianBlur(Frame, (5, 5), 0)
                cv.imshow("Frame", BlurImage)
                DecodeBarcode = pyzbar.decode(Frame)
                if DecodeBarcode == []:
                    print("Fant ingen barcode")
                else:
                    for i in DecodeBarcode:
                        Barcode = i.data
                Key = cv.waitKey(1)
                if (Key == ord("q")):
                    print("Programmet avsluttet")
                    break
                if (Key == ord("c")):
                    ean = self.EAN(Barcode)
                    BarcodeName = ean.save('barcodes/' + Barcode)
                    ImageName = "images/{}.jpg".format(Barcode)
                    if (ImageName == 'images/.jpg'):
                        pass
                    else:
                        cv.imwrite(ImageName, BlurImage)
                        print("{} Lagret".format(ImageName))
                        Count += 1
            else:

                Ret = False
                break


if __name__ == '__main__':
    """
        Setter noen spesial variaber som __name__ og kjører all av koden som fant seg i filen
        Lager 2 variable
        EAN: class(code39)
        Capture = webkamera som er koblet til pc-en 
        1 for webkamera 
        0 for innebygde kamera på pc-en
        Kaller klassen og gir verdi for variablene så kaller den andre funskjonen for å kjøre programmet

    """
    EAN = barcode.get_barcode_class('code39')
    Capture = cv.VideoCapture(1)
    CaptureFrame(EAN, Capture).getFrame()