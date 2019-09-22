from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

traffic_line_max = 4
traffic_line_min = -traffic_line_max

safety_dist = 2


class Car:
    def __init__(self):
        self.appear_frame = -1
        self.start_road = -1
        self.finish_road = -1
        self.velocity1 = -1
        self.velocity2 = -1
        
        self.loc = np.array([0.0, 0.0, 0.0])
        self.vel = np.array([0.0, 0.0, 0.0])
        self.radius = 0.3
        self.mass = 1.0
        
        self.force = np.array([0., 0., 0.])
        self.gravity = np.array([0., 0., 0.])
        self.colPlane = np.array([0., 0.5, 0., 0.])

        self.latency = 0.0
    
    def set_appear_frame(self, appear_frame):
        self.appear_frame = float(appear_frame)
    def set_start_road(self, road):
        self.start_road = road
    def set_finish_road(self, road):
        self.finish_road = road
    def set_velocity1(self, velocity):
        self.velocity1 = velocity
    def set_velocity2(self, velocity):
        self.velocity2 = velocity
    def set_loc(self, loc):
        self.loc = loc
    def set_vel(self, vel):
        self.vel = vel
        
    def set_car(self, appear_frame, start_road, finish_road, velocity1, velocity2):
        self.set_appear_frame(appear_frame)
        self.set_start_road(start_road)
        self.set_finish_road(finish_road)
        self.set_velocity1(velocity1)
        self.set_velocity2(velocity2)
    
    def get_appear_frame(self):
        return self.appear_frame
    def get_start_road(self):
        return self.start_road
    def get_finish_road(self):
        return self.finish_road
    def get_velocity1(self):
        return self.velocity1
    def get_velocity2(self):
        return self.velocity2
    def get_loc(self):
        return self.loc
    def get_vel(self):
        return self.vel
    def get_latency(self):
        return self.latency
    
    def print_car(self):
        print("appear frame : ", self.appear_frame)
        print("start road : ", self.start_road)
        print("finish road : ", self.finish_road)
        print("velocity1 : ", self.velocity1)
        print("velocity2 : ", self.velocity2)
        print("latency : ", self.latency)

    def draw(self, et):
        # y val correction
        self.loc[1] = 0.5

        run_frame = et * 60
        if run_frame >= self.appear_frame:
            glPushMatrix()
            glColor([1.0, 0.0, 0.0])
            glTranslatef(self.loc[0], self.loc[1], self.loc[2])
            glutSolidSphere(self.radius, 20, 20)
            glPopMatrix()

    def set(self, loc, vel=np.array([0., 0., 0.])):
        self.loc = loc
        self.vel = vel
        
    def setColPlane(self, N, d):
        self.colPlane[0] = N[0]
        self.colPlane[1] = N[1]
        self.colPlane[2] = N[2]
        self.colPlane[3] = d
    
    def setRadius(self, r):
        self.radius = r

    def setMass(self, m):
        self.mass = m
        self.radius = m**(1.0/3.0)

    def setGravity(self, g):
        self.gravity = g

    def addForce(self, f):
        self.force += f

    def resetForce(self):
        self.force = np.array([0., 0., 0.])

    def simulate(self, et, dt):
        run_frame = et * 60
        if run_frame >= self.appear_frame:
            acc = self.gravity + self.force / self.mass
            self.vel = self.vel + acc*dt
            self.loc = self.loc + self.vel*dt

    def corner(self):
        # from bottom
        if self.start_road == 0:
            if self.finish_road == 1:
                if self.loc[2] <= -1.0:
                    self.loc = np.array([self.loc[0], self.loc[1], -1.0])
                    self.vel = np.array([-self.velocity2, 0.0, 0.0])
            elif self.finish_road == 3:
                if self.loc[2] <= 1.0:
                    self.loc = np.array([self.loc[0], self.loc[1], 1.0])
                    self.vel = np.array([self.velocity2, 0.0, 0.0])
        # from left
        elif self.start_road == 1:
            if self.finish_road == 2:
                if self.loc[0] >= 1.0:
                    self.loc = np.array([1.0, self.loc[1], self.loc[2]])
                    self.vel = np.array([0.0, 0.0, -self.velocity2])
            elif self.finish_road == 0:
                if self.loc[0] >= -1.0:
                    self.loc = np.array([-1.0, self.loc[1], self.loc[2]])
                    self.vel = np.array([0.0, 0.0, self.velocity2])
        # from up
        elif self.start_road == 2:
            if self.finish_road == 3:
                if self.loc[2] >= 1.0:
                    self.loc = np.array([self.loc[0], self.loc[1], 1.0])
                    self.vel = np.array([self.velocity2, 0.0, 0.0])
            elif self.finish_road == 1:
                if self.loc[2] >= -1.0:
                    self.loc = np.array([self.loc[0], self.loc[1], -1.0])
                    self.vel = np.array([-self.velocity2, 0.0, 0.0])
        # from right
        else: # self.start_road == 3
            if self.finish_road == 0:
                if self.loc[0] <= -1.0:
                    self.loc = np.array([-1.0, self.loc[1], self.loc[2]])
                    self.vel = np.array([0.0, 0.0, self.velocity2])
            elif self.finish_road == 2:
                if self.loc[0] <= 1.0:
                    self.loc = np.array([1.0, self.loc[1], self.loc[2]])
                    self.vel = np.array([0.0, 0.0, -self.velocity2])

    def computeForce(self, other):
        l0 = self.loc
        l1 = other.loc
        m0 = self.mass
        m1 = other.mass
        dir = l1-l0
        r   = np.linalg.norm(dir)
        dir = dir/r
        G = 40.5
        force = (G * m1*m0 / (r**2.0)) *dir
        return force

    def colHandlePair(self, other):
        l0 = self.loc
        l1 = other.loc
        m0 = self.mass
        m1 = other.mass
        v0 = self.vel
        v1 = other.vel
        r0 = self.radius
        r1 = other.radius
        R = r0+r1

        # after collision
        N = l0 - l1
        dist = np.linalg.norm(N)
        N = N/dist

        e = 0.0

        if dist < R: # collision
            penetration = R - dist
            l0 += (0.5+0.5*e)*penetration * N
            l1 -= (0.5+0.5*e)*penetration * N
            Vrel = v0 - v1
            if np.dot(Vrel, N) < 0:
                # processing collision(update velocity)
                M = m0 + m1
                vp0 = np.dot(N, v0)
                vp1 = np.dot(N, v1)

                J = (1 + e) * (vp1 - vp0) * m0 * m1 / M

                v0new =  J / m0 + vp0
                v1new = -J / m1 + vp1

                self.vel = self.vel - vp0 * N + v0new * N
                other.vel = other.vel - vp1 * N + v1new * N

        # before collision
        elif (dist >= R) and (dist <= R + safety_dist):
            if l1[0] == 1.0:  # x = 1.0 # from bottom
                if l0[0] == 1.0:
                    if (l0[2] < l1[2]) and (l0[2] >= l1[2] - safety_dist): # only for safe distance
                        other.vel[2] = self.vel[2]
            if l1[2] == 1.0: # z = 1.0 # from left
                if l0[2] == 1.0:
                    if (l0[0] > l1[0]) and (l0[0] <= l1[0] + safety_dist):
                        other.vel[0] = self.vel[0]
            if l1[0] == -1.0: # x = -1.0 # from up
                if l0[0] == -1.0: # x = -1.0
                    if (l0[2] > l1[2]) and (l0[2] <= l1[2] + safety_dist):
                        other.vel[2] = self.vel[2]
            if l1[2] == -1.0: # z = -1.0 # from right
                if l0[2] == -1.0:
                    if (l0[0] < l1[0]) and (l0[0] >= l1[0] - safety_dist):
                        other.vel[0] = self.vel[0]

    def colHandle(self, traffic_light):
        # col with bottom
        if self.colPlane is None :
            return

        N = np.array([self.colPlane[0], self.colPlane[1], self.colPlane[2]])
        d = self.colPlane[3]
        p0 = d*N

        u = self.loc - p0

        penetration = -np.dot(u, N)
        e = 0.7

        if penetration > -self.radius: # the center through into plane.
            penetration += self.radius
            self.loc += (1+e)*penetration*N
            penVel = -np.dot(self.vel, N)
            if penVel > 0:
                self.vel = self.vel + (1.+e)*penVel*N

        # col with traffic
        traffic_line = np.array([traffic_line_min, traffic_line_max])
        if self.start_road == 0 or self.start_road == 2:  # from bottom, up
            if (self.loc[2] >= traffic_line[0]) and (self.loc[2] <= traffic_line[1]):
                if self.start_road == 0:
                    if traffic_light != 0:
                        self.vel[2] = 0.0
                    else:
                        self.vel[2] = -self.velocity1
                else:
                    if traffic_light != 2:
                        self.vel[2] = 0.0
                    else:
                        self.vel[2] = self.velocity1
            else:
                if self.start_road == 0:
                    if traffic_light == 0:
                        self.vel[2] = -self.velocity1
                else:
                    if traffic_light == 2:
                        self.vel[2] = self.velocity1

        else: # from left, right
            if (self.loc[0] >= traffic_line[0]) and (self.loc[0] <= traffic_line[1]):
                if self.start_road == 1:
                    if traffic_light != 1:
                        self.vel[0] = 0.0
                    else:
                        self.vel[0] = self.velocity1
                else: # start road == 3 # from right
                    if traffic_light != 3:
                        self.vel[0] = 0.0
                    else:
                        self.vel[0] = -self.velocity1
            else:
                if self.start_road == 1:
                    if traffic_light == 1:
                        self.vel[0] = self.velocity1
                else:
                    if traffic_light == 3:
                        self.vel[0] = -self.velocity1

    def cal_latency(self, dt):
        if self.start_road == 0 and self.start_road == 2:
            if self.vel[2] == 0.0:
                self.latency += dt
        else: # start road == 1 or 3
            if self.vel[0] == 0.0:
                self.latency += dt

