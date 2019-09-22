from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class Traffic:
    def __init__(self):
        self.light_on_order = []
        self.light_on = 0

        self.loc0 = np.array([3.0, 0.5, 10.0])
        self.loc1 = np.array([-10.0, 0.5, 3.0])
        self.loc2 = np.array([-3.0, 0.5, -10.0])
        self.loc3 = np.array([10.0, 0.5, -3.0])

        self.whole_duration = 30
        self.durations = np.array([0.0, 0.0, 0.0, 0.0])

        self.start_time = 0.0
        self.finish_time = 0.0

    def set_light_on_order(self, light_on_order):
        self.light_on_order = light_on_order

    def set_light_on(self, light_on):
        self.light_on = light_on

    def set_whole_duration(self, whole_duration):
        self.whole_duration = whole_duration

    def set_durations(self, durs):
        self.durations = durs

    def set(self, nums_of_cars):
        whole_cars = sum(nums_of_cars)
        per_of_cars0 = float(nums_of_cars[0]) / whole_cars
        per_of_cars1 = float(nums_of_cars[1]) / whole_cars
        per_of_cars2 = float(nums_of_cars[2]) / whole_cars
        per_of_cars3 = float(nums_of_cars[3]) / whole_cars

        dur_of_road0 = self.whole_duration * per_of_cars0
        dur_of_road1 = self.whole_duration * per_of_cars1
        dur_of_road2 = self.whole_duration * per_of_cars2
        dur_of_road3 = self.whole_duration * per_of_cars3
        durs = np.array([dur_of_road0, dur_of_road1, dur_of_road2, dur_of_road3])
        self.set_durations(durs)

        light_on_order = []
        for i in range(len(nums_of_cars)):
            max_index = nums_of_cars.index(max(nums_of_cars))
            light_on_order.append(max_index)

            nums_of_cars[max_index] = -1

        self.set_light_on_order(light_on_order)
        self.set_light_on(self.light_on_order[0])
        print('light on order : ', self.light_on_order)

    def get_whole_duration(self):
        return self.whole_duration

    def get_light_on(self):
        return self.light_on

    def draw(self):
        glPushMatrix()
        glColor([0.5, 0.5, 0.5])
        if self.light_on == 0:
            glColor([0.0, 1.0, 0.1])
        glTranslatef(self.loc0[0], self.loc0[1], self.loc0[2])
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glColor([0.5, 0.5, 0.5])
        if self.light_on == 1:
            glColor([0.0, 1.0, 0.1])
        glTranslatef(self.loc1[0], self.loc1[1], self.loc1[2])
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glColor([0.5, 0.5, 0.5])
        if self.light_on == 2:
            glColor([0.0, 1.0, 0.1])
        glTranslatef(self.loc2[0], self.loc2[1], self.loc2[2])
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glColor([0.5, 0.5, 0.5])
        if self.light_on == 3:
            glColor([0.0, 1.0, 0.1])
        glTranslatef(self.loc3[0], self.loc3[1], self.loc3[2])
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

    def simulate(self, dt):
        current_dur = self.durations[self.light_on]

        self.finish_time += dt
        if self.finish_time - self.start_time >= current_dur:
            self.start_time = self.finish_time
            self.light_on = self.light_on_order[(self.light_on_order.index(self.light_on) + 1) % len(self.light_on_order)]

    def get_traffic_times(self, et):
        return et / self.whole_duration
