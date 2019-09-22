import numpy as np

class Object:
    def __init__(self):
        self.id = -1
        self.type = -1
        self.frame_list = [] # 등장 프레임 기록
        self.point_list =  [] # 각 프레임에서의 위치 기록
        
    def set_id(self, id):
        self.id = float(id)
    def set_type(self, type):
        self.type = type
    def append_frame(self, frame):
        self.frame_list.append(float(frame))
    def append_point(self, point):
        self.point_list.append(np.array(point))
        
    def set_object(self, id, type, frame, point):
        self.set_id(id)
        self.set_type(type)
        self.append_frame(frame)
        self.append_point(point)
            
    def get_id(self):
        return self.id
    def get_type(self):
        return self.type
    def get_frame_list(self):
        return self.frame_list
    def get_appear_frame(self):
        return self.frame_list[0]
    def get_disappear_frame(self):
        return self.frame_list[len(self.frame_list) - 1]
    def get_point_list(self):
        return self.point_list
    def get_start_point(self):
        return self.point_list[0]
    def get_finish_point(self):
        return self.point_list[len(self.point_list) - 1]
    