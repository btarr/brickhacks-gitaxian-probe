import card_list
import cv2
import config
import math
import numpy as np
import pytesseract
import re
import requests
import Levenshtein
import os

IMAGE_PATH1 = 'test_images/52392543_10215967629041766_4399718357188739072_n.jpg'
IMAGE_PATH2 = 'test_images/51910856_10218669713956123_7599104603388379136_n.jpg'
IMAGE_PATH3 = 'test_images/Screen Shot 2019-02-17 at 12.49.00 AM.jpg'
IMAGE_PATH4 = '/Users/hanksheehan/brickhacks-gitaxian-probe/src/test_images/Screen Shot 2019-202-17 at 12.49.00 AM.jpg'
ANGLE_THRESHOLD = 20
CARD_WIDTH = 488.0
CARD_HEIGHT = 680.0
BOUNDING_THRESH = 100

def get_price(card_name):
    headers = {'Accept': 'application/json', 'Authorization': 'bearer {}'.format(config.token)}

    url = "http://api.tcgplayer.com/v1.19.0/catalog/products"
    querystring = {"productName": card_name}

    response = requests.request("GET", url, params=querystring, headers=headers)

    productId = response.json()['results'][0]['productId']

    url = "http://api.tcgplayer.com/v1.19.0/pricing/product/{}".format(productId)

    response = requests.request("GET", url, headers=headers)
    return '${}'.format(response.json()['results'][0]['marketPrice'])


def sort_corners(corners):
    # Find the top left
    left_to_right = sorted(corners, key=lambda corner: corner[0][0])
    top_to_bottom = sorted(corners, key=lambda corner: corner[0][1])

    left_top, right_top, right_bottom, left_bottom = np.array([[0,0]]),np.array([[0,0]]),np.array([[0,0]]),np.array([[0,0]])

    for index1 in range(len(left_to_right)):
        for index2 in range(len(top_to_bottom)):
            if np.array_equal(left_to_right[index1], top_to_bottom[index2]):
                if index1 < 2 and index2 < 2:
                    left_top = left_to_right[index1]
                elif index1 < 2 and index2 >= 2:
                    left_bottom = left_to_right[index1]
                elif index1 >= 2 and index2 >= 2:
                    right_bottom = left_to_right[index1]
                elif index1 >= 2 and index2 < 2:
                    right_top = left_to_right[index1]

    return np.array([left_top, right_top, right_bottom, left_bottom])


def is_card_dimentions(points):
    width = (points[1][0][0] - points[0][0][0] + points[2][0][0] - points[3][0][0])/2
    height = (points[3][0][1] - points[0][0][1] + points[2][0][1] - points[1][0][1])/2
    return (CARD_WIDTH+BOUNDING_THRESH)/CARD_HEIGHT > float(width)/height > CARD_WIDTH/(CARD_HEIGHT+BOUNDING_THRESH)


def is_subrectangle(rectangle, rectangle_list):
    for rect in rectangle_list:
        for point in rectangle:
            x_values, y_values = cv2.split(rect)
            x_values = sorted(x_values, key=lambda value: value[0])
            x_min = x_values[0][0]
            x_max = x_values[-1][0]
            y_values = sorted(y_values, key=lambda value: value[0])
            y_min = y_values[0][0]
            y_max = y_values[-1][0]

            if (x_max > point[0][0] > x_min and y_max > point[0][1] > y_min):
                return True

    return False


def crop_image(input_image):
    img = np.copy(input_image)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_threshold = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

    contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda contour: cv2.contourArea(contour), reverse=True)

    # Filter by size
    contours = filter(lambda contour: 10000 < cv2.contourArea(contour), contours)

    visited_contours = []

    for index in range(len(contours)):
        contour = contours[index]
        epsilon = 0.1*cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,epsilon,True)

        if len(approx) == 4 and not is_subrectangle(approx, visited_contours) and is_card_dimentions(sort_corners(approx)):
            visited_contours.append(sort_corners(approx))

            cv2.drawContours(img_threshold,[approx],0,(255,0,0),2)

            approx = sort_corners(approx)
            flat = np.array([ [0,0],[488,0],[488,680], [0,680] ],np.float32)
            transform = cv2.getPerspectiveTransform(approx.astype(np.float32),flat)
            warp = cv2.warpPerspective(img_gray,transform,(488,680))
            # cv2.imshow('{}'.format(index), warp)


            name_img = warp[0:80,15:400]
            cv2.imshow('name', name_img)

            _, name_img = cv2.threshold(name_img, 130, 200, cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
            # cv2.imshow('name', name_img)
            # cv2.imshow('{} name'.format(index), name_img)
            cv2.imwrite('tmp/name.png', name_img)
            os.system('convert -units PixelsPerInch tmp/name.png -density 144 tmp/name.png')
            name = os.popen('tesseract tmp/name.png stdout').read().strip()
            name = re.sub('\W+', '', name)

            if name:
                closest = float('inf')
                closest_name = ''
                for card in sorted(card_list.card_list, key=lambda card: -len(card)):
                    dist = Levenshtein.distance(card.encode('utf-8').strip(), name.encode('utf-8').strip())
                    if dist < closest:
                        closest = dist
                        closest_name = card

                price = ''
                try:
                    price = get_price(closest_name)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img,'{}'.format(closest_name),tuple(approx[0][0] + np.array([30,50])), font, .5,(255,255,255),2,cv2.LINE_AA)
                    cv2.putText(img,'{}'.format(price),tuple(approx[0][0] + np.array([30,100])), font, .5,(255,255,255),2,cv2.LINE_AA)
                except:
                    pass

                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            # cv2.moveWindow('{}'.format(index), index*300, 0)

    cv2.imshow('img', img)
    cv2.waitKey(0)

if __name__ == '__main__':
    # cap = cv2.VideoCapture(0)
    # while(True):
        # Capture frame-by-frame
        # ret, frame = cap.read()
        # crop_image(frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    crop_image(cv2.imread(IMAGE_PATH1))
    crop_image(cv2.imread(IMAGE_PATH2))
    crop_image(cv2.imread(IMAGE_PATH3))
    crop_image(cv2.imread(IMAGE_PATH4))


    # get_price("Celestial Colonnade")
