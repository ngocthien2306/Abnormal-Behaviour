import cv2
class Camera:
  
    def __init__(self, camera):
        self.camera = camera
        self.vc = None

    def open(self, width=640, height=480, fps=30):
        self.vc = cv2.VideoCapture(0)
        

        self.width = width
        self.height = height
        self.fps = fps
        # vc.set(5, fps)  #set FPS
        self.vc.set(3, width)   # set width
        self.vc.set(4, height)  # set height

        return self.vc.isOpened()

    def read(self, negative=False):
        rval, frame = self.vc.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            if negative:
                frame = cv2.bitwise_not(frame)
            return frame

    def read_gray(self, negative=False):            
        rval, frame = self.vc.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB) 
            if negative:
                frame = cv2.bitwise_not(frame)
            return frame