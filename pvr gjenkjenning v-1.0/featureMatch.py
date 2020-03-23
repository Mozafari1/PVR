# Dette er gjenkjennings programmet

# importerer noen nødvendige pakker 
import numpy as np
import cv2
import glob

#Fjerner innholdet i filene før programmet skriver i filene. 
cleanPercentFile = open("percent/percent.txt", "r+")
cleanPercentFile.seek(0)
cleanPercentFile.truncate()
cleanNameFile = open("imageName/name.txt", "r+")
cleanNameFile.seek(0)
cleanNameFile.truncate()

#leser inn bildet med OpenCV
original = cv2.imread("singleImage/A4 C-0000 A.jpg")

#Lager SURF objekt og spesifiserer noen nødvendige parametrene og setter Hessian Threshold til 2000
sift = cv2.xfeatures2d.SURF_create(2000)
# Finner de viktige punkter og beskriver det direkte i det bildet som sammenlignes med bilder i databsen
kp_1, desc_1 = sift.detectAndCompute(original, None)
#Flann parameters 
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)
# Lager to tomt array og legger bilder og navn i arrayet fra filen "images"
all_images_to_compare = []
titles = []
for f in glob.iglob("images/*"):

    image = cv2.imread(f)
    titles.append(f)
    all_images_to_compare.append(image)
percentiage = 0
# Her finner jeg de viktige punktene og beskrivelse av bildene som var i filen images
for image_to_compare, title in zip(all_images_to_compare, titles):

    kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
    #print("Kp1: " + str(len(kp_1)))
    #print("Kp2: " + str(len(kp_2)))  # 1 med 30

    matches = flann.knnMatch(desc_1, desc_2, k=2)
# Her bruker jeg forholdstest 
    good_points = []
    for m, n in matches:
        if m.distance < 0.4 * n.distance:
            good_points.append(m)
    number_keypoints = 0
#Tilstand
    if len(kp_1) > len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)
# skriver i filer
    percentiage = len(good_points) * 100 / number_keypoints
    f = open("percent/percent.txt", "a")
    f.write("{:.0f}\n".format(percentiage))
    n = open("imageName/name.txt", "a")
    print >> n, title
    n.close()
# leser fra filen 
    print("Filnavn:" + title)
    f = open("percent/percent.txt", "r+")
    nums = f.readlines()
    nums = [int(i) for i in nums]
    w = (max(nums))
#Sjekker tilstanden og tegner match punktene
    if percentiage == w:
        print("Match percent: {0:.1f}%".format(percentiage))
        result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2,
                                 good_points, None)
        img = cv2.resize(result, None, fx=0.3, fy=0.3)

        cv2.imshow("The result image", img)
        cv2.imwrite("result/result.jpg", result)
    else:
        print("Match percent: {0:.1f}%".format(percentiage))
