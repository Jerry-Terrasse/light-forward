import cv2
import time
import queue
import logging

logger = logging.getLogger(__name__)

class UIEvent:
    SWIPE = 0
    
    def __init__(self, event: int, info) -> None:
        self.event = event
        self.info = info
    def __repr__(self) -> str:
        return f"UIEvent({self.event}, {self.info})"

class UI:
    def __init__(self, name: str, width: int = None, height: int = None) -> None:
        self.name = name
        self.winname = f"W_{name}"
        
        self.width = width if width else 800
        self.height = height if height else 450
        self.scale = 1.
        self.press: tuple[tuple[int, int], float] | None = None
        
        self.events: queue.Queue[UIEvent] = queue.Queue()

        cv2.namedWindow(self.winname, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(self.winname, self.on_mouse)
    
    def on_mouse(self, event: int, x: int, y: int, flags: int, param) -> None:
        x, y = int(x / self.scale), int(y / self.scale)
        logger.debug(f"on_mouse: {event}, {x}, {y}, {flags}, {param}")
        if event == cv2.EVENT_LBUTTONDOWN:
            self.press = (x, y), time.time()
            return
        if event == cv2.EVENT_LBUTTONUP:
            if self.press is None:
                return
            (px, py), pt = self.press
            self.events.put(UIEvent(UIEvent.SWIPE, ((px, py), (x, y), time.time() - pt)))
            self.press = None
            return
        
    def auto_resize(self, img):
        self.scale = min(self.width / img.shape[1], self.height / img.shape[0], 1)
        w, h = int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)
        return cv2.resize(img, (w, h))
    
    def display(self, img, delay: int = 1):
        img = self.auto_resize(img)
        cv2.imshow(self.winname, img)
        return cv2.waitKey(delay)

    def get_event(self) -> UIEvent | None:
        try:
            return self.events.get_nowait()
        except queue.Empty:
            return None