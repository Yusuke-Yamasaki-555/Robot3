import cv2
import numpy as np

def getMask(frame, l, u):
    # HSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    lower = np.array(l)
    upper = np.array(u)
    if lower[0] >= 0:
        #色相が正の値のとき、赤以外のマスク
        mask = cv2.inRange(hsv, lower, upper)
    else:
        #色相が負の値のとき、赤用マスク
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < lower[0]*-1) | h > upper[0]) & (s > lower[1]) & (s < upper[1]) & (v > lower[2]) & (v < upper[2])] = 255
 
    return cv2.bitwise_and(frame, frame, mask = mask)

def getContours(frame, img, t, r, color):
    colors = {"R":(0, 0, 255), "G":(0, 255, 0), "B":(255, 0, 0), "Y":(0, 255, 255)}
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    # 一番大きい輪郭を抽出
    contours.sort(key=cv2.contourArea, reverse=True)
    # print(contours)
    #一つ以上検出
    if len(contours) > 0:
    #     for cnt in contours:
            # 最小外接円を描く
        # (x,y), radius = cv2.minEnclosingCircle(contours[0])
        # center = (int(x),int(y))
        # radius = int(radius)
    
        # if radius > r:
        #     frame = cv2.circle(frame,center,radius,colors[color],2)
        # else:
        #     pass
        x,y,w,h = cv2.boundingRect(contours[0])
        if w >= 50 and h >= 50:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),colors[color],2)
    return frame

def main():
    cap = cv2.VideoCapture(0)
    red_l = [-10,128,0]
    red_u = [170,255,255]
    yellow_l = [20, 80, 10]
    yellow_u = ([50, 255, 255])
    while True:
        _, frame = cap.read()
        # frame = cv2.resize(frame, dsize = None, fx = 1, fy = 1)
        res_red = getMask(frame, red_l, red_u)
        contours_frame = getContours(frame, res_red, 40, 5, color="R") # (画像, 明度閾値, 最小半径)
        res_yellow = getMask(frame, yellow_l, yellow_u)
        contours_frame = getContours(contours_frame, res_yellow, 50, 30, color="Y") # (画像, 明度閾値, 最小半径)
        

        cv2.imshow('video', contours_frame)
        k = cv2.waitKey(5) & 0XFF
        if k == 27: 
            cap.release()
            break
    return 0

if __name__ == "__main__":
    main()
