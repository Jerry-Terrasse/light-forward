from paddleocr import PaddleOCR
import logging
logging.getLogger("ppocr").setLevel(logging.ERROR)

from itertools import chain


# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
# img_path = '/home/terrasse/Downloads/ppocr_img/imgs/11.jpg'
# result = ocr.ocr(img_path, cls=True)
# for idx in range(len(result)):
#     res = result[idx]
#     for line in res:
#         print(line)

# 显示结果
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

def extrace_text(img):
    result: list[list[tuple[list[tuple[float, float]], tuple[str, float]]]] = ocr.ocr(img)
    items = [(box, text, score) for box, (text, score) in chain.from_iterable(filter(None, result)) if score > 0.7]
    return items