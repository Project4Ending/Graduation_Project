#!/usr/bin/env python
# coding: utf-8

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

import CGGame
import Car
import Traffic

safety_dist = 30


def find_by_frame(cars, frame):
    for car in cars:
        if car.appear_frame == frame:
            return car


def sort_by_frame(cars):
    appear_frames = []
    for car in cars:
        appear_frames.append(car.appear_frame)
    appear_frames.sort()

    temp = []
    for frame in appear_frames:
        temp.append(find_by_frame(cars, frame))
    return temp


# 전역 변수
prgm_start_time = 0
prgm_finish_time = 0

avg_latency_list = []  # 차량 평균 대기시간
traffic_times_list = []  # 신호 회전양
whole_dur_list = []  # traffics 전체 지속시간

dur_delta = 5

class myGame(CGGame.Game):

    def __init__(self, w, h, title):
        prgm_start_time = time.time()

        super(myGame, self).__init__(w, h, title)

        self.cars = []
        self.traffics = Traffic.Traffic()

        self.from_bottom = [] # start_road == 0
        self.from_left = [] # start_raod == 1
        self.from_up = [] # start_road == 2
        self.from_right = [] # start_road == 3

        self.init_cars()
        self.init_traffics()

        self.avg_latency = 0
        self.traffic_times = 0

    def init_cars(self):
        self.cars = []  # 초기화
        self.from_bottom = []
        self.from_left = []
        self.from_up = []
        self.from_right = []

        input_path = './cars_data.csv'
        
        cars_data = pd.read_csv(input_path)
        
        appear_frame_col = cars_data['appear_frame']
        start_road_col = cars_data['start_road']
        finish_road_col = cars_data['finish_road']
        velocity1_col = cars_data['velocity1']
        velocity2_col = cars_data['velocity2']

        # 객체 생성
        for i in range(len(cars_data)):
            new_car = Car.Car()

            appear_frame = appear_frame_col[i]
            start_road = start_road_col[i]
            finish_road = finish_road_col[i]
            velocity1 = velocity1_col[i] * 60 # vel per frame -> vel per sec
            velocity2 = velocity2_col[i] * 60 # vel per frame -> vel per sec

            # velocity 1, 2 가 0인 경우 제외
            if velocity1 == 0 or velocity2 == 0:
                continue

            new_car.set_car(appear_frame, start_road, finish_road, velocity1, velocity2)
            self.cars.append(new_car)

            # 이동 도로에 따라 차량 분류
            if start_road == 0:
                self.from_bottom.append(new_car)
            elif start_road == 1:
                self.from_left.append(new_car)
            elif start_road == 2:
                self.from_up.append(new_car)
            else : # start_road == 3
                self.from_right.append(new_car)

        # 객체 분류
        for car in self.cars:
            # 차량 초기화 결과 확인
            if car.get_velocity1() == 0 or car.get_velocity2() == 0:
                exit()
            car.setGravity(np.array([0., -9.8, 0.]))

        # 차량의 정보에 따라 시작위치 초기화
        # Z축 : +가 화면 앞, -가 화면 뒤
        i = 0
        for car in self.from_bottom:
            loc = np.array([1.0, 0.5, (30.0 + i*safety_dist)])
            vel = np.array([0.0, 0.0, -car.get_velocity1()])
            car.set(loc, vel)
            i += 1
        i = 0
        for car in self.from_left:
            loc = np.array([-(30 + i*safety_dist), 0.5, 1.0])
            vel = np.array([car.get_velocity1(), 0.0, 0.0])
            car.set(loc, vel)
            i += 1
        i = 0
        for car in self.from_up:
            loc = np.array([-1.0, 0.5, -(30.0 + i*safety_dist)])
            vel = np.array([0.0, 0.0, car.get_velocity1()])
            car.set(loc, vel)
            i += 1
        i = 0
        for car in self.from_right:
            loc = np.array([(30 + i*safety_dist), 0.5, -1.0])
            vel = np.array([-car.get_velocity1(), 0.0, 0.0])
            car.set(loc, vel)
            i += 1
        i = 0

        # 전체 차량 개수 확인
        print('whole cars : ', len(self.cars)) # 40개
        print('from bottom cars : ', len(self.from_bottom))
        print('from left cars : ', len(self.from_left))
        print('from up cars : ', len(self.from_up))
        print('from right cars : ', len(self.from_right))

        self.cars = sort_by_frame(self.cars)
        self.from_bottom = sort_by_frame(self.from_bottom)
        self.from_left = sort_by_frame(self.from_left)
        self.from_up = sort_by_frame(self.from_up)
        self.from_right = sort_by_frame(self.from_right)
        return

    def init_traffics(self):
        num_from_bottom = len(self.from_bottom)
        num_from_left = len(self.from_left)
        num_from_up = len(self.from_up)
        num_from_right = len(self.from_right)
        nums_of_cars = [num_from_bottom, num_from_left, num_from_up, num_from_right]

        self.traffics.set(nums_of_cars)


    def frame(self):
        dt = self.getDt()
        et = self.getEt()

        super(myGame, self).frame()

        # cars
        traffic_light = self.traffics.get_light_on()

        for car in self.cars:
            car.corner()
            car.simulate(et, dt)
            car.colHandle(traffic_light)
            car.cal_latency(dt)

         # 충돌을 세팅, 탄성계수 0.1
        for i in range(len(self.cars) - 1):
            for j in range(i+1, len(self.cars)):
                self.cars[i].colHandlePair(self.cars[j])

        for car in self.cars:
            car.draw(et)

        # traffics
        self.traffics.simulate(dt)
        self.traffics.draw()

        # latency
        for car in self.cars:
            self.avg_latency += car.get_latency()
        self.avg_latency /= len(self.cars)
        self.traffic_times = self.traffics.get_traffic_times(et)
        print('average latency : ', self.avg_latency)
        print('traffic runs : ', self.traffic_times)

        # check loop
        is_loop_over = True
        for car in self.cars:
            if car.finish_road == 0:  # to bottom
                if car.loc[2] < 100:
                    is_loop_over = False
            elif car.finish_road == 1:  # to left
                if car.loc[0] > -100:
                    is_loop_over = False
            elif car.finish_road == 2:  # to up
                if car.loc[2] > -100:
                    is_loop_over = False
            else:  # finish road == 3 # to right
                if car.loc[0] < 100:
                    is_loop_over = False
        print('is loop over ? : ', is_loop_over)

        # set next stage
        if is_loop_over:
            avg_latency_list.append(self.avg_latency)
            traffic_times_list.append(self.traffic_times)

            cur_whole_dur = self.traffics.get_whole_duration()
            whole_dur_list.append(cur_whole_dur)

            self.init_cars()
            self.init_traffics()

            next_whole_dur = cur_whole_dur - dur_delta
            self.traffics.set_whole_duration(next_whole_dur)
            self.timerReset()

            # loop 종료 조건
            if next_whole_dur <= 0:
                prgm_finish_time = time.time()

                # plt
                fig = plt.figure()
                plot1 = fig.add_subplot(2, 1, 1) # 지속시간
                plot2 = fig.add_subplot(2, 1, 2) # 신호 회전률

                plot1.title.set_text('[duration, avg latency]')
                plot2.title.set_text('[duration, traffic times]')

                plot1.plot(whole_dur_list, avg_latency_list)
                plot2.plot(whole_dur_list, traffic_times_list)

                plt.show()

                # conclusion
                min_avg_latency_idx = avg_latency_list.index(min(avg_latency_list))
                most_efficient_dur = whole_dur_list[min_avg_latency_idx]
                traffic_times = traffic_times_list[min_avg_latency_idx]

                prgm_run_time = prgm_finish_time - prgm_start_time
                print('----------conculusion----------')
                print('program run time : ', prgm_run_time)
                print('most efficient duration : ', most_efficient_dur)
                print('with ', traffic_times, ' traffic times')
                print('-------------------------------')

                exit()

        super(myGame, self).afterFrame()

game = myGame(700,700, b"simul")
game.grid(True)


def key(k, x,y):
    if k is b't':
        if game.timer.timerRunning:
            game.timerStop()
        else:
            game.timerStart()
    if k is b'r':
        game.init_cars()
        game.init_traffics()


def draw():
    game.frame()

game.start(draw, key)




