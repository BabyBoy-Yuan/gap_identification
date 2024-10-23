from PIL import Image
import cv2

bg_img = cv2.imread('./bigimage.jpg')
tp_img = cv2.imread('./smallimage.jpg')
bg_edge = cv2.Canny(bg_img, 100, 200)
tp_edge = cv2.Canny(tp_img, 100, 200)
cv2.imwrite('1.jpg', bg_edge) # 保存在本地
cv2.imwrite('2.jpg', tp_edge) # 保存在本地

bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
X = max_loc[0]
print(X)
print(max_loc[1])
th, tw = tp_pic.shape[:2]
tl = max_loc # 左上角点的坐标

br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标

cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形

cv2.imwrite('out.jpg', bg_img) # 保存在本地


