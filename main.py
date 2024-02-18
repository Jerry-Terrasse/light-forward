from airtest.core.api import init_device, G
import logging
logging.getLogger("airtest").setLevel(logging.ERROR)

import cv2
from PIL import ImageDraw, Image, ImageFont
import numpy as np
import time

from detect.ocr import extrace_text
from ui.ui import UI, UIEvent


# connect an android phone with adb
init_device("Android")
# or use connect_device api
# connect_device("Android:///")

# install("path/to/your/apk")
# start_app("package_name_of_your_apk")
# touch(Template("image_of_a_button.png"))
# swipe(Template("slide_start.png"), Template("slide_end.png"))
# assert_exists(Template("success.png"))
# keyevent("BACK")
# home()
# uninstall("package_name_of_your_apk")

ui = UI("ui", 1600, 900)

while True:
    begin_t = time.time()
    
    screen = G.DEVICE.snapshot()
    textes = extrace_text(screen)
    
    canvas = np.zeros_like(screen)
    for box, text, score in textes:
        box = np.array(box, dtype=np.int32)
        cv2.polylines(canvas, [box], isClosed=True, color=(0, 255, 0), thickness=1)
        # cv2.putText(canvas, text, (box[0][0], box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # put text in box
        h = box[3][1] - box[0][1]
        h *= 0.9
        # text_size, baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        # text_scale = h / text_size[1]
        # cv2.putText(canvas, text, (box[0][0], box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, text_scale, (0, 255, 0), 2)
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        fontText = ImageFont.truetype("./fonts/simfang.ttf", h, encoding="utf-8")
        draw.text((box[0][0], box[0][1]), text, (255, 255, 255), font=fontText)
        canvas = np.array(pil_img)

        while e := ui.get_event():
            if e.event == UIEvent.SWIPE:
                (x1, y1), (x2, y2), t = e.info
                G.DEVICE.swipe((x1, y1), (x2, y2), t)
        
        end_t = time.time()
        print(f"fps: {1 / (end_t - begin_t)}")
    
    ui.display(canvas)
    
    # time.sleep(1)