#importerer nødvendige pakker
import cv2
import barcode
import pyzbar.pyzbar as pyzbar
#Fant ut at TE bruker barcode "code39"
EAN = barcode.get_barcode_class('code39')

cap = cv2.VideoCapture(1)

count = 0
bar_code = ''
#Denne delen av programmet leser barkode og tar bilde og
#lagrer i to separate filer hvor den en er barcode og en andre bilder
#Bildet tas ved å trykke på knappen "c" og avslutes med "q"
#Hvis det er ingen frame/bilderamme som programmet avsluttes auto
while True:

    if cap.isOpened():
        ret, frame = cap.read()
        blur = cv2.GaussianBlur(frame, (5, 5), 0)
        cv2.imshow("Frame", blur)
        decode = pyzbar.decode(frame)

        if decode == []:
            pass
        else:
            for i in decode:
                bar_code = i.data

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

        if key == ord("c"):

            ean = EAN(bar_code)  # ean code 39
            fullname = ean.save('barcode/' + bar_code)

            img_name = "images/{}.jpg".format(bar_code)
            cv2.imwrite(img_name, blur)
            print("{} lagret".format(img_name))
            count += 1

    else:
        ret = False

        break
