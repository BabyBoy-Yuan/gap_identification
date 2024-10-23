import cv2
import time
import base64
import redis
import requests


class capcode(object):

    def __init__(self):
        self.capcode_url = "http://www.sqfgc.com:80/sqfc/publish/lp/getImageVerifyCode.do"
        self.redis_pool()

    def redis_pool(self):
        pool = redis.ConnectionPool(host='192.168.187.132', port=6379, decode_responses=True, db=1)
        self.conn= redis.Redis(connection_pool=pool)

    def save_image(self, image_name, image_base64):
        image_bytes = base64.b64decode(image_base64)
        with open(f'./{image_name}.jpg', 'wb+') as fp:
            fp.write(image_bytes)

    def get_capcode(self):
        response = requests.post(url=self.capcode_url)
        if response.status_code == 200:
            dataInfo = response.json().get("dataInfo").get("dataInfo")
            capcode = dataInfo.get('capcode')
            smallImage = dataInfo.get('smallImage')
            bigImage = dataInfo.get('bigImage')
            self.save_image(image_name='smallImage', image_base64=smallImage)
            self.save_image(image_name='bigImage', image_base64=bigImage)
            return capcode

    def shibei(self):
        bg_img = cv2.imread('./bigimage.jpg')
        tp_img = cv2.imread('./smallimage.jpg')
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        X = max_loc[0]
        Y = max_loc[1]
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite('out.jpg', bg_img)  # 保存在本地
        return X, Y

    def start(self):
        # capcode=self.get_capcode()
        # X, Y = self.shibei()
        # code = capcode + ";" + str(X)
        # key_name = int(time.time()*1000000).__str__()
        # print(key_name)
        # # self.conn.set(key_name, code, ex=5)
        # self.conn.set(key_name, code)
        names = self.conn.randomkey()  # 随机取值
        codes = self.conn.get(names)
        print(codes)

if __name__ == '__main__':
    capcode().start()