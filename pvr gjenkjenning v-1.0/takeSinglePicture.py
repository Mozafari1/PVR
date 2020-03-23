#importerer pakke
import cv2


cap = cv2.VideoCapture(1)

# Denne delen av programmet tar et bildet og og etter bildet er tatt så kan gjenkjennings programmet states for å sammenligne bildet
# Når bildet er gjenkjent så brukern kan ta nytt bildet. fila overskrives med samme navn
while True:
    if cap.isOpened():
        ret, frame = cap.read()

        blur = cv2.GaussianBlur(frame, (5, 5), 0)

        cv2.imshow("Frame", blur)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

        if key == ord("c"):

            img_name = "singleImage/A4 C-0000 A.jpg"
            cv2.imwrite(img_name, blur)
            print("{} lagret".format(img_name))

    else:
        ret = False
        break
