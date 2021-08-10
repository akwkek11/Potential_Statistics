'''
    Coded by Cho_bo

    potentialtable.py
        - 잠재능력 테이블 생성, 반환

    2021-08-09 ~
'''
from typing import List

class table:
    def __init__(self) -> None:
        self.first_weight_index: int = 0
        self.down_weight_index: int = 0
        
        '''
            공/마 : p_power9, p_power12, m_power9, m_power12
            보공 : boss20, boss30, boss35, boss40
            방무 : def30, def35, def40
            피격 : attacked - (20, 40 합친 확률)

            레드 큐브와 블랙 큐브는 현재 가중치 자체는 동일하다.
            하지만, 각각의 큐브마다 가중치는 달라질 수 있는 가능성이 존재하기에,
            레드 큐브/블랙 큐브는 중복 로직이여도 따로 연산하게끔 분류해두었다.

            에디셔널 큐브는 현재 기준 단 한 종류.
        '''
        
        '''
            윗잠, 레드 큐브, 이전 확률
        '''
        # 가중치 순서는 공격력, 마력, 보공, 방무 순이므로, 홈페이지는 방무 - 보공 순이니 헷갈리지 말자.

        # 무기
        self.weapon_option_first: list = ['p_power12', 'm_power12', 'boss30', 'boss35', 'boss40', 'def35', 'def40', 'etc']
        self.weapon_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'boss20', 'boss30', 'boss35', 'boss40', 'def30', 'def35', 'def40', 'etc']
        self.weapon_option_third: list = self.weapon_option_second[:]
        self.weapon_option_weight_first: list = [1, 1, 1, 1, 1, 1, 1, 13.5]
        self.weapon_option_weight_second: list = [1.5, 1.5, 1.5, 1, 1.5, 15.5]
        self.weapon_option_weight_third: list = self.weapon_option_weight_second[:]
        self.weapon_option_prob_first: list = []
        self.weapon_option_prob_second: list = []
        self.weapon_option_prob_third: list = []

        for i in range(len(self.weapon_option_first) - 1):
            self.weapon_option_prob_first.append(round(self.weapon_option_weight_first[i] / sum(self.weapon_option_weight_first), 6))
        for i in range(len(self.weapon_option_second) - 1):
            if i in [2, 3, 4, 5, 8]:
                self.weapon_option_prob_second.append(round(0.9 * self.weapon_option_weight_second[self.down_weight_index] / sum(self.weapon_option_weight_second), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10]:
                if i == len(self.weapon_option_prob_second) - 1:
                    self.weapon_option_prob_second[i] += round(0.1 * self.weapon_option_weight_first[self.first_weight_index] / sum(self.weapon_option_weight_first), 6)
                else:
                    self.weapon_option_prob_second.append(round(0.1 * self.weapon_option_weight_first[self.first_weight_index] / sum(self.weapon_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.weapon_option_third) - 1):
            if i in [2, 3, 4, 5, 8]:
                self.weapon_option_prob_third.append(round(0.99 * self.weapon_option_weight_third[self.down_weight_index] / sum(self.weapon_option_weight_third), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10]:
                if i == len(self.weapon_option_prob_third) - 1:
                    self.weapon_option_prob_third[i] += round(0.01 * self.weapon_option_weight_first[self.first_weight_index] / sum(self.weapon_option_weight_first), 6)
                else:
                    self.weapon_option_prob_third.append(round(0.01 * self.weapon_option_weight_first[self.first_weight_index] / sum(self.weapon_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        weapon_option_prob_first: list = [0.04878, 0.04878, 0.04878, 0.04878, 0.04878, 0.04878, 0.04878]
        weapon_option_prob_second: list = [0.004878, 0.004878, 0.06, 0.06, 0.06, 0.044878, 0.004878, 0.004878, 0.06, 0.004878, 0.004878]
        weapon_option_prob_third: list = [0.000488, 0.000488, 0.066, 0.066, 0.066, 0.044488, 0.000488, 0.000488, 0.066, 0.000488, 0.000488]
        '''

        self.weapon_option_prob_first.append(1 - sum(self.weapon_option_prob_first))
        self.weapon_option_prob_second.append(1 - sum(self.weapon_option_prob_second))
        self.weapon_option_prob_third.append(1 - sum(self.weapon_option_prob_third))

        # 보조무기
        self.subweapon_option_first: list = ['p_power12', 'm_power12', 'boss30', 'boss35', 'boss40', 'def35', 'def40', 'attacked', 'etc']
        self.subweapon_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'boss20', 'boss30', 'boss35', 'boss40', 'def30', 'def35', 'def40', 'attacked', 'etc']
        self.subweapon_option_third: list = self.subweapon_option_second[:]
        self.subweapon_option_weight_first: list = [1, 1, 1, 1, 1, 1, 1, 3, 13.5]
        self.subweapon_option_weight_second: list = [1.5, 1.5, 1.5, 1, 1.5, 4, 15.5]
        self.subweapon_option_weight_third: list = self.subweapon_option_weight_second[:]
        self.subweapon_option_prob_first: list = []
        self.subweapon_option_prob_second: list = []
        self.subweapon_option_prob_third: list = []
        
        for i in range(len(self.subweapon_option_first) - 1):
            self.subweapon_option_prob_first.append(round(self.subweapon_option_weight_first[i] / sum(self.subweapon_option_weight_first), 6))
        for i in range(len(self.subweapon_option_second) - 1):
            if i in [2, 3, 4, 5, 8, 11]:
                self.subweapon_option_prob_second.append(round(0.9 * self.subweapon_option_weight_second[self.down_weight_index] / sum(self.subweapon_option_weight_second), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10, 11]:
                if i == len(self.subweapon_option_prob_second) - 1:
                    self.subweapon_option_prob_second[i] += round(0.1 * self.subweapon_option_weight_first[self.first_weight_index] / sum(self.subweapon_option_weight_first), 6)
                else:
                    self.subweapon_option_prob_second.append(round(0.1 * self.subweapon_option_weight_first[self.first_weight_index] / sum(self.subweapon_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.subweapon_option_third) - 1):
            if i in [2, 3, 4, 5, 8, 11]:
                self.subweapon_option_prob_third.append(round(0.99 * self.subweapon_option_weight_third[self.down_weight_index] / sum(self.subweapon_option_weight_third), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10, 11]:
                if i == len(self.subweapon_option_prob_third) - 1:
                    self.subweapon_option_prob_third[i] += round(0.01 * self.subweapon_option_weight_first[self.first_weight_index] / sum(self.subweapon_option_weight_first), 6)
                else:
                    self.subweapon_option_prob_third.append(round(0.01 * self.subweapon_option_weight_first[self.first_weight_index] / sum(self.subweapon_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        subweapon_option_prob_first: list = [0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.12766]
        subweapon_option_prob_second: list = [0.004255, 0.004255, 0.050943, 0.050943, 0.050943, 0.038217, 0.004255, 0.004255, 0.050943, 0.004255, 0.004255, 0.14436]
        subweapon_option_prob_third: list = [0.000426, 0.000426, 0.056038, 0.056038, 0.056038, 0.037784, 0.000426, 0.000426, 0.056038, 0.000426, 0.000426, 0.15071]
        '''

        self.subweapon_option_prob_first.append(1 - sum(self.subweapon_option_prob_first))
        self.subweapon_option_prob_second.append(1 - sum(self.subweapon_option_prob_second))
        self.subweapon_option_prob_third.append(1 - sum(self.subweapon_option_prob_third))

        # 엠블럼
        self.emblem_option_first: list = ['p_power12', 'm_power12', 'def35', 'def40', 'etc']
        self.emblem_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'def30', 'def35', 'def40', 'etc']
        self.emblem_option_third: list = self.emblem_option_second[:]
        self.emblem_option_weight_first: list = [1, 1, 1, 1, 13.5]
        self.emblem_option_weight_second: list = [1, 1, 1, 10.333333]
        self.emblem_option_weight_third: list = self.emblem_option_weight_second[:]
        self.emblem_option_prob_first: list = []
        self.emblem_option_prob_second: list = []
        self.emblem_option_prob_third: list = []

        for i in range(len(self.emblem_option_first) - 1):
            self.emblem_option_prob_first.append(round(self.emblem_option_weight_first[i] / sum(self.emblem_option_weight_first), 6))
        for i in range(len(self.emblem_option_second) - 1):
            if i in [2, 3, 4]:
                self.emblem_option_prob_second.append(round(0.9 * self.emblem_option_weight_second[self.down_weight_index] / sum(self.emblem_option_weight_second), 6))
                self.down_weight_index += 1
            else:
                self.emblem_option_prob_second.append(round(0.1 * self.emblem_option_weight_first[self.first_weight_index] / sum(self.emblem_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.emblem_option_third) - 1):
            if i in [2, 3, 4]:
                self.emblem_option_prob_third.append(round(0.99 * self.emblem_option_weight_third[self.down_weight_index] / sum(self.emblem_option_weight_third), 6))
                self.down_weight_index += 1
            else:
                self.emblem_option_prob_third.append(round(0.01 * self.emblem_option_weight_first[self.first_weight_index] / sum(self.emblem_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        emblem_option_prob_first: list = [0.057143, 0.057143, 0.057143, 0.057143]
        emblem_option_prob_second: list = [0.005714, 0.005714, 0.0675, 0.0675, 0.0675, 0.005714, 0.005714]
        emblem_option_prob_third: list = [0.000571, 0.000571, 0.07425, 0.07425, 0.07425, 0.000571, 0.000571]
        '''

        self.emblem_option_prob_first.append(1 - sum(self.emblem_option_prob_first))
        self.emblem_option_prob_second.append(1 - sum(self.emblem_option_prob_second))
        self.emblem_option_prob_third.append(1 - sum(self.emblem_option_prob_third))
        
        '''
            윗잠, 블랙 큐브, 이전 확률
        '''

        # 무기
        self.weapon_black_option_first: list = ['p_power12', 'm_power12', 'boss30', 'boss35', 'boss40', 'def35', 'def40', 'etc']
        self.weapon_black_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'boss20', 'boss30', 'boss35', 'boss40', 'def30', 'def35', 'def40', 'etc']
        self.weapon_black_option_third: list = self.weapon_black_option_second[:]
        self.weapon_black_option_weight_first: list = [1, 1, 1, 1, 1, 1, 1, 13.5]
        self.weapon_black_option_weight_second: list = [1.5, 1.5, 1.5, 1, 1.5, 15.5]
        self.weapon_black_option_weight_third: list = self.weapon_black_option_weight_second[:]
        self.weapon_black_option_prob_first: list = []
        self.weapon_black_option_prob_second: list = []
        self.weapon_black_option_prob_third: list = []

        for i in range(len(self.weapon_black_option_first) - 1):
            self.weapon_black_option_prob_first.append(round(self.weapon_black_option_weight_first[i] / sum(self.weapon_black_option_weight_first), 6))
        for i in range(len(self.weapon_black_option_second) - 1):
            if i in [2, 3, 4, 5, 8]:
                self.weapon_black_option_prob_second.append(round(0.8 * self.weapon_black_option_weight_second[self.down_weight_index] / sum(self.weapon_black_option_weight_second), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10]:
                if i == len(self.weapon_black_option_prob_second) - 1:
                    self.weapon_black_option_prob_second[i] += round(0.2 * self.weapon_black_option_weight_first[self.first_weight_index] / sum(self.weapon_black_option_weight_first), 6)
                else:
                    self.weapon_black_option_prob_second.append(round(0.2 * self.weapon_black_option_weight_first[self.first_weight_index] / sum(self.weapon_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.weapon_black_option_third) - 1):
            if i in [2, 3, 4, 5, 8]:
                self.weapon_black_option_prob_third.append(round(0.95 * self.weapon_black_option_weight_third[self.down_weight_index] / sum(self.weapon_black_option_weight_third), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10]:
                if i == len(self.weapon_black_option_prob_third) - 1:
                    self.weapon_black_option_prob_third[i] += round(0.05 * self.weapon_black_option_weight_first[self.first_weight_index] / sum(self.weapon_black_option_weight_first), 6)
                else:
                    self.weapon_black_option_prob_third.append(round(0.05 * self.weapon_black_option_weight_first[self.first_weight_index] / sum(self.weapon_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        weapon_black_option_prob_first: list = [0.04878, 0.04878, 0.04878, 0.04878, 0.04878, 0.04878, 0.04878]
        weapon_black_option_prob_second: list = [0.009576, 0.009756, 0.053333, 0.053333, 0.053333, 0.045312, 0.009756, 0.009756, 0.053333, 0.009756, 0.009756]
        weapon_black_option_prob_third: list = [0.002439, 0.002439, 0.063333, 0.063333, 0.063333, 0.044661, 0.002439, 0.002439, 0.063333, 0.002439, 0.002439]
        '''

        self.weapon_black_option_prob_first.append(1 - sum(self.weapon_black_option_prob_first))
        self.weapon_black_option_prob_second.append(1 - sum(self.weapon_black_option_prob_second))
        self.weapon_black_option_prob_third.append(1 - sum(self.weapon_black_option_prob_third))

        # 보조무기
        self.subweapon_black_option_first: list = ['p_power12', 'm_power12', 'boss30', 'boss35', 'boss40', 'def35', 'def40', 'attacked', 'etc']
        self.subweapon_black_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'boss20', 'boss30', 'boss35', 'boss40', 'def30', 'def35', 'def40', 'attacked', 'etc']
        self.subweapon_black_option_third: list = self.subweapon_black_option_second[:]
        self.subweapon_black_option_weight_first: list = [1, 1, 1, 1, 1, 1, 1, 3, 13.5]
        self.subweapon_black_option_weight_second: list = [1.5, 1.5, 1.5, 1, 1.5, 4, 15.5]
        self.subweapon_black_option_weight_third: list = self.subweapon_black_option_weight_second[:]
        self.subweapon_black_option_prob_first: list = []
        self.subweapon_black_option_prob_second: list = []
        self.subweapon_black_option_prob_third: list = []
        
        for i in range(len(self.subweapon_black_option_first) - 1):
            self.subweapon_black_option_prob_first.append(round(self.subweapon_black_option_weight_first[i] / sum(self.subweapon_black_option_weight_first), 6))
        for i in range(len(self.subweapon_black_option_second) - 1):
            if i in [2, 3, 4, 5, 8, 11]:
                self.subweapon_black_option_prob_second.append(round(0.8 * self.subweapon_black_option_weight_second[self.down_weight_index] / sum(self.subweapon_black_option_weight_second), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10, 11]:
                if i == len(self.subweapon_black_option_prob_second) - 1:
                    self.subweapon_black_option_prob_second[i] += round(0.2 * self.subweapon_black_option_weight_first[self.first_weight_index] / sum(self.subweapon_black_option_weight_first), 6)
                else:
                    self.subweapon_black_option_prob_second.append(round(0.2 * self.subweapon_black_option_weight_first[self.first_weight_index] / sum(self.subweapon_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.subweapon_black_option_third) - 1):
            if i in [2, 3, 4, 5, 8, 11]:
                self.subweapon_black_option_prob_third.append(round(0.95 * self.subweapon_black_option_weight_third[self.down_weight_index] / sum(self.subweapon_black_option_weight_third), 6))
                self.down_weight_index += 1
            if i in [0, 1, 5, 6, 7, 9, 10, 11]:
                if i == len(self.subweapon_black_option_prob_third) - 1:
                    self.subweapon_black_option_prob_third[i] += round(0.05 * self.subweapon_black_option_weight_first[self.first_weight_index] / sum(self.subweapon_black_option_weight_first), 6)
                else:
                    self.subweapon_black_option_prob_third.append(round(0.05 * self.subweapon_black_option_weight_first[self.first_weight_index] / sum(self.subweapon_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        subweapon_black_option_prob_first: list = [0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.042553, 0.12766]
        subweapon_black_option_prob_second: list = [0.008511, 0.008511, 0.045283, 0.045283, 0.045283, 0.0387, 0.008511, 0.008511, 0.045283, 0.008511, 0.008511, 0.146286]
        subweapon_black_option_prob_third: list = [0.002128, 0.002128, 0.053374, 0.053374, 0.053374, 0.037977, 0.002128, 0.002128, 0.053374, 0.002128, 0.002128, 0.149778]
        '''

        self.subweapon_black_option_prob_first.append(1 - sum(self.subweapon_black_option_prob_first))
        self.subweapon_black_option_prob_second.append(1 - sum(self.subweapon_black_option_prob_second))
        self.subweapon_black_option_prob_third.append(1 - sum(self.subweapon_black_option_prob_third))

        # 엠블럼
        self.emblem_black_option_first: list = ['p_power12', 'm_power12', 'def35', 'def40', 'etc']
        self.emblem_black_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'def30', 'def35', 'def40', 'etc']
        self.emblem_black_option_third: list = self.emblem_black_option_second[:]
        self.emblem_black_option_weight_first: list = [1, 1, 1, 1, 13.5]
        self.emblem_black_option_weight_second: list = [1, 1, 1, 10.333333]
        self.emblem_black_option_weight_third: list = self.emblem_black_option_weight_second[:]
        self.emblem_black_option_prob_first: list = []
        self.emblem_black_option_prob_second: list = []
        self.emblem_black_option_prob_third: list = []

        for i in range(len(self.emblem_black_option_first) - 1):
            self.emblem_black_option_prob_first.append(round(self.emblem_black_option_weight_first[i] / sum(self.emblem_black_option_weight_first), 6))
        for i in range(len(self.emblem_black_option_second) - 1):
            if i in [2, 3, 4]:
                self.emblem_black_option_prob_second.append(round(0.8 * self.emblem_black_option_weight_second[self.down_weight_index] / sum(self.emblem_black_option_weight_second), 6))
                self.down_weight_index += 1
            else:
                self.emblem_black_option_prob_second.append(round(0.2 * self.emblem_black_option_weight_first[self.first_weight_index] / sum(self.emblem_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0
        for i in range(len(self.emblem_black_option_third) - 1):
            if i in [2, 3, 4]:
                self.emblem_black_option_prob_third.append(round(0.95 * self.emblem_black_option_weight_third[self.down_weight_index] / sum(self.emblem_black_option_weight_third), 6))
                self.down_weight_index += 1
            else:
                self.emblem_black_option_prob_third.append(round(0.05 * self.emblem_black_option_weight_first[self.first_weight_index] / sum(self.emblem_black_option_weight_first), 6))
                self.first_weight_index += 1
        self.first_weight_index = 0
        self.down_weight_index = 0

        '''
        emblem_black_option_prob_first: list = [0.057143, 0.057143, 0.057143, 0.057143]
        emblem_black_option_prob_second: list = [0.011429, 0.011429, 0.06, 0.06, 0.06, 0.011429, 0.011429]
        emblem_black_option_prob_third: list = [0.002857, 0.002857, 0.07125, 0.07125, 0.07125, 0.002857, 0.002857]
        '''

        self.emblem_black_option_prob_first.append(1 - sum(self.emblem_black_option_prob_first))
        self.emblem_black_option_prob_second.append(1 - sum(self.emblem_black_option_prob_second))
        self.emblem_black_option_prob_third.append(1 - sum(self.emblem_black_option_prob_third))
        
        '''
            윗잠, 레드 큐브, 이후 확률
        '''

        '''
            윗잠, 블랙 큐브, 이후 확률
        '''

        '''
            에디셔널
        '''

        # 무기

        # 보조무기

        # 엠블럼

    # 레드 큐브
    def getWeapon(self) -> List[list]:
        '''
            무기 - 레드 큐브
        '''
        return [self.weapon_option_first, self.weapon_option_second, self.weapon_option_third, 
                self.weapon_option_prob_first, self.weapon_option_prob_second, self.weapon_option_prob_third]
    
    def getSubweapon(self) -> List[list]:
        '''
            보조무기 - 레드 큐브
        '''
        return [self.subweapon_option_first, self.subweapon_option_second, self.subweapon_option_third, 
                self.subweapon_option_prob_first, self.subweapon_option_prob_second, self.subweapon_option_prob_third]

    def getEmblem(self) -> List[list]:
        '''
            엠블럼 - 레드 큐브
        '''
        return [self.emblem_option_first, self.emblem_option_second, self.emblem_option_third,
                self.emblem_option_prob_first, self.emblem_option_prob_second, self.emblem_option_prob_third]

    # 블랙 큐브
    def getBlackweapon(self) -> List[list]:
        '''
            무기 - 블랙 큐브
        '''
        return [self.weapon_black_option_first, self.weapon_black_option_second, self.weapon_black_option_third, 
                self.weapon_black_option_prob_first, self.weapon_black_option_prob_second, self.weapon_black_option_prob_third]
    
    def getBlacksubweapon(self) -> List[list]:
        '''
            보조무기 - 블랙 큐브
        '''
        return [self.subweapon_black_option_first, self.subweapon_black_option_second, self.subweapon_black_option_third, 
                self.subweapon_black_option_prob_first, self.subweapon_black_option_prob_second, self.subweapon_black_option_prob_third]

    def getBlackemblem(self) -> List[list]:
        '''
            엠블럼 - 블랙 큐브
        '''
        return [self.emblem_black_option_first, self.emblem_black_option_second, self.emblem_black_option_third,
                self.emblem_black_option_prob_first, self.emblem_black_option_prob_second, self.emblem_black_option_prob_third]
