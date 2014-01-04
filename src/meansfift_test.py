import numpy as np
import cv2


cap = cv2.VideoCapture('../data/Vid_A_Ball.avi')
# take first frame of the video
ret,frame = cap.read()


# setup initial location of window
r,h,c,w = (110,  55, 200, 50)  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h,c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0 )

print frame.shape
while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)


        x,y,w,h = track_window
        roi = hsv[y:y+h,x:x+w]
        mask = cv2.inRange(roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        hist = cv2.calcHist([roi],[0],mask,[180],[0,180])

        # Draw it on image
        cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2', frame)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            img2.shape
            break

    else:
        break

cv2.destroyAllWindows()
cap.release()