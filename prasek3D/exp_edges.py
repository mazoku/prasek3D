from __future__ import division

import numpy as np
import cv2
import skimage.morphology as skimor
import skimage.measure as skimea
import pymorph as pm

import os

if __name__ == '__main__':
    cnt_area_T = 10
    winname = 'contours'
    trackbarname = 'area'
    data_dir = '/home/tomas/Dropbox/Data/Kana'
    use_trackbar = False

    # get all the files in given directory
    root, __, files = os.walk(data_dir).next()
    img_paths = [os.path.join(root, x) for x in files]

    # -------------------
    def update(dummy=None):
        cat = cv2.getTrackbarPos(trackbarname, 'contours')
        cnts_f = [c for c in cnts if cv2.contourArea(c) > cat]
        img_vis = image.copy()
        cv2.drawContours(img_vis, cnts_f, -1, (255, 0, 255), 1)
        cv2.imshow(winname, img_vis)

    # load the image and append it to the protos list
    for img_path in img_paths:
        image = cv2.imread(img_path)

        # fname = '/home/tomas/Dropbox/Data/Kana/3Dprasek-1_02-1000x2.png'
        # image = cv2.imread(fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        blurred = cv2.medianBlur(gray, 5)
        # blurred = gray

        tight = cv2.Canny(blurred, 10, 30)

        print 'thinning ...',
        sk1 = 255 * skimor.thin(tight).astype(np.uint8)
        print 'done'

        print 'contours ...',
        cnts = cv2.findContours(tight.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        print 'done'

        # bez trackbaru
        if not use_trackbar:
            img_vis = np.zeros(gray.shape)
            cnts_f = [c for c in cnts if cv2.contourArea(c) > cnt_area_T]
            cv2.drawContours(img_vis, cnts_f, -1, 255, 1)

            out_fname = img_path.replace('.tif', '_edges.tif')
            cv2.imwrite(out_fname, img_vis)

            cv2.imshow(winname, img_vis)
            cv2.waitKey(0)
        else:
            update()
            cv2.createTrackbar(trackbarname, winname, 0, 500, update)

            while True:
                ch = 0xFF & cv2.waitKey()
                if ch == 27:
                    break
            cv2.destroyAllWindows()