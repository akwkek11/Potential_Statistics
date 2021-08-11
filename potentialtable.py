'''
    Coded by Cho_bo

    potentialtable.py
        - 잠재능력 테이블 생성, 반환

    2021-08-09 ~
'''
from typing import List

class table:
    def createTable(self, 
                    first_option: list, second_option: list, third_option: list, 
                    first_weight: list, second_weight: list, third_weight: list, 
                    first_prob: list, second_prob: list, third_prob: list, 
                    first_target: list, second_and_third_target: list, cube: int) -> None:
        '''
            큐브 테이블 생성

            input
                - option : 각각 1, 2, 3번째 옵션 테이블
                - weight : 각각 1, 2, 3번째 가중치
                - prob : 각각 가중치에 의해 생성된 확률 리스트
                - target : n번째 옵션이 1번째 가중치인지, 아니면 2/3번째 가중치인지 분류
                - cube : 
                    cube_dict: dict = {'red': 0, 'black': 1, 'additional': 2}
                    enum을 그대로 따라간다.

            output
                - prob list 3개에 append되어 들어간다.
        '''
        second_prob_dict: dict = {0 : 0.1, 1: 0.2, 2: 0.004975}
        third_prob_dict: dict = {0 : 0.01, 1: 0.05, 2: 0.004975}

        second_prob_constant: float = second_prob_dict[cube]
        third_prob_constant: float = third_prob_dict[cube]
        for i in range(len(first_option) - 1):
            first_prob.append(round(first_weight[i] / sum(first_weight), 6))
        
        first_weight_index: int = 0
        down_weight_index: int = 0
        for i in range(len(second_option) - 1):
            if i in first_target:
                second_prob.append(round((1 - second_prob_constant) * second_weight[down_weight_index] / sum(second_weight), 6))
                down_weight_index += 1
            if i in second_and_third_target:
                if i == len(second_prob) - 1:
                    second_prob[i] += round(second_prob_constant * first_weight[first_weight_index] / sum(first_weight), 6)
                else:
                    second_prob.append(round(second_prob_constant * first_weight[first_weight_index] / sum(first_weight), 6))
                first_weight_index += 1

        first_weight_index = 0
        down_weight_index = 0
        for i in range(len(third_option) - 1):
            if i in first_target:
                third_prob.append(round((1 - third_prob_constant) * third_weight[down_weight_index] / sum(third_weight), 6))
                down_weight_index += 1
            if i in second_and_third_target:
                if i == len(third_prob) - 1:
                    third_prob[i] += round(third_prob_constant * first_weight[first_weight_index] / sum(first_weight), 6)
                else:
                    third_prob.append(round(third_prob_constant * first_weight[first_weight_index] / sum(first_weight), 6))
                first_weight_index += 1

        return

    def __init__(self) -> None:
        '''
            공/마 : p_power9, p_power12, m_power9, m_power12 / 랩당 공/마는 phy+1, mag+1
            보공 : boss20, boss30, boss35, boss40 / 에디 한정 boss18, boss12
            방무 : def30, def35, def40 / 에디 한정 def5, def4
            피격 : attacked - (20, 40 합친 확률)
            
            힘 : str12, str9 / 랩당 힘은 str+2, str+1
            덱 : dex12, dex9 / 랩당 덱은 dex+2, dex+1
            인 : int12, int9 / 랩당 인은 int+2, int+1
            럭 : luk12, luk9 / 랩당 럭은 luk+2, luk+1

            레드 큐브와 블랙 큐브는 현재 가중치 자체는 동일하다.
            하지만, 각각의 큐브마다 가중치는 달라질 수 있는 가능성이 존재하기에,
            레드 큐브/블랙 큐브는 중복 로직이여도 따로 연산하게끔 분류해두었다.

            에디셔널 큐브는 현재 기준 단 한 종류.
        '''
        
        '''
            윗잠, 레드 큐브, 이전 확률
        '''
        # 가중치 순서는 공격력, 마력, 보공, 방무 순이므로, 홈페이지는 방무 - 보공 순이니 헷갈리지 말자.

        cube_dict: dict = {'red': 0, 'black': 1, 'additional': 2}

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

        self.createTable(self.weapon_option_first, self.weapon_option_second, self.weapon_option_third,
                         self.weapon_option_weight_first, self.weapon_option_weight_second, self.weapon_option_weight_third,
                         self.weapon_option_prob_first, self.weapon_option_prob_second, self.weapon_option_prob_third,
                         [2, 3, 4, 5, 8], [0, 1, 5, 6, 7, 9, 10], cube=cube_dict['red'])
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
        
        self.createTable(self.subweapon_option_first, self.subweapon_option_second, self.subweapon_option_third,
                         self.subweapon_option_weight_first, self.subweapon_option_weight_second, self.subweapon_option_weight_third,
                         self.subweapon_option_prob_first, self.subweapon_option_prob_second, self.subweapon_option_prob_third,
                         [2, 3, 4, 5, 8, 11], [0, 1, 5, 6, 7, 9, 10, 11], cube=cube_dict['red'])
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

        self.createTable(self.emblem_option_first, self.emblem_option_second, self.emblem_option_third,
                         self.emblem_option_weight_first, self.emblem_option_weight_second, self.emblem_option_weight_third,
                         self.emblem_option_prob_first, self.emblem_option_prob_second, self.emblem_option_prob_third,
                         [2, 3, 4], [0, 1, 5, 6], cube=cube_dict['red'])
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

        self.createTable(self.weapon_black_option_first, self.weapon_black_option_second, self.weapon_black_option_third,
                         self.weapon_black_option_weight_first, self.weapon_black_option_weight_second, self.weapon_black_option_weight_third,
                         self.weapon_black_option_prob_first, self.weapon_black_option_prob_second, self.weapon_black_option_prob_third,
                         [2, 3, 4, 5, 8], [0, 1, 5, 6, 7, 9, 10], cube=cube_dict['black'])
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
        
        self.createTable(self.subweapon_black_option_first, self.subweapon_black_option_second, self.subweapon_black_option_third,
                         self.subweapon_black_option_weight_first, self.subweapon_black_option_weight_second, self.subweapon_black_option_weight_third,
                         self.subweapon_black_option_prob_first, self.subweapon_black_option_prob_second, self.subweapon_black_option_prob_third,
                         [2, 3, 4, 5, 8, 11], [0, 1, 5, 6, 7, 9, 10, 11], cube=cube_dict['black'])
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

        self.createTable(self.emblem_black_option_first, self.emblem_black_option_second, self.emblem_black_option_third,
                         self.emblem_black_option_weight_first, self.emblem_black_option_weight_second, self.emblem_black_option_weight_third,
                         self.emblem_black_option_prob_first, self.emblem_black_option_prob_second, self.emblem_black_option_prob_third,
                         [2, 3, 4], [0, 1, 5, 6], cube=cube_dict['black'])
        '''
        emblem_black_option_prob_first: list = [0.057143, 0.057143, 0.057143, 0.057143]
        emblem_black_option_prob_second: list = [0.011429, 0.011429, 0.06, 0.06, 0.06, 0.011429, 0.011429]
        emblem_black_option_prob_third: list = [0.002857, 0.002857, 0.07125, 0.07125, 0.07125, 0.002857, 0.002857]
        '''

        self.emblem_black_option_prob_first.append(1 - sum(self.emblem_black_option_prob_first))
        self.emblem_black_option_prob_second.append(1 - sum(self.emblem_black_option_prob_second))
        self.emblem_black_option_prob_third.append(1 - sum(self.emblem_black_option_prob_third))
        
        '''
            윗잠, 레드 큐브, 이후 확률, 패치 이후 추가할 것
        '''

        '''
            윗잠, 블랙 큐브, 이후 확률, 패치 이후 추가할 것
        '''

        '''
            에디셔널
        '''

        # 무기
        self.additional_weapon_option_first: list = ['p_power12', 'm_power12', 'critical12', 
                                                     'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                     'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                     'Def5', 'boss18', 'etc']
        self.additional_weapon_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'critical12', 'critical9',
                                                      'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                      'str9', 'dex9', 'int9', 'luk9', 'damage9', 'all6',
                                                      'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                      'Str+1', 'Dex+1', 'Int+1', 'Luk+1',
                                                      'Def5', 'Def4', 'boss18', 'boss12', 'etc']
        self.additional_weapon_option_third: list = self.additional_weapon_option_second[:]
        self.additional_weapon_option_weight_first: list = [1, 1, 1, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 3.5]
        self.additional_weapon_option_weight_second: list = [1, 1, 1, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 6]
        self.additional_weapon_option_weight_third: list = self.additional_weapon_option_weight_second[:]
        self.additional_weapon_option_prob_first: list = []
        self.additional_weapon_option_prob_second: list = []
        self.additional_weapon_option_prob_third: list = []

        self.createTable(self.additional_weapon_option_first, self.additional_weapon_option_second, self.additional_weapon_option_third,
                         self.additional_weapon_option_weight_first, self.additional_weapon_option_weight_second, self.additional_weapon_option_weight_third,
                         self.additional_weapon_option_prob_first, self.additional_weapon_option_prob_second, self.additional_weapon_option_prob_third,
                         [2, 3, 5, 12, 13, 14, 15, 16, 17, 24, 25, 26, 27, 29, 31], 
                         [0, 1, 4, 6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23, 28, 30], 
                         cube=cube_dict['additional'])

        self.additional_weapon_option_prob_first.append(1 - sum(self.additional_weapon_option_prob_first))
        self.additional_weapon_option_prob_second.append(1 - sum(self.additional_weapon_option_prob_second))
        self.additional_weapon_option_prob_third.append(1 - sum(self.additional_weapon_option_prob_third))

        # 보조무기
        self.additional_subweapon_option_first: list = ['p_power12', 'm_power12', 'critical12', 'Cridamage1',
                                                        'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                        'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                        'Def5', 'boss18', 'etc']
        self.additional_subweapon_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'critical12', 'critical9', 'Cridamage1',
                                                         'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                         'str9', 'dex9', 'int9', 'luk9', 'damage9', 'all6',
                                                         'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                         'Str+1', 'Dex+1', 'Int+1', 'Luk+1',
                                                         'Def5', 'Def4', 'boss18', 'boss12', 'etc']
        self.additional_subweapon_option_third: list = self.additional_subweapon_option_second[:]
        self.additional_subweapon_option_weight_first: list = [1, 1, 1, 1, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 3.5]
        self.additional_subweapon_option_weight_second: list = [1, 1, 1, 1.5, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 6]
        self.additional_subweapon_option_weight_third: list = self.additional_subweapon_option_weight_second[:]
        self.additional_subweapon_option_prob_first: list = []
        self.additional_subweapon_option_prob_second: list = []
        self.additional_subweapon_option_prob_third: list = []

        self.createTable(self.additional_subweapon_option_first, self.additional_subweapon_option_second, self.additional_subweapon_option_third,
                         self.additional_subweapon_option_weight_first, self.additional_subweapon_option_weight_second, self.additional_subweapon_option_weight_third,
                         self.additional_subweapon_option_prob_first, self.additional_subweapon_option_prob_second, self.additional_subweapon_option_prob_third,
                         [2, 3, 5, 13, 14, 15, 16, 17, 18, 25, 26, 27, 28, 30, 32], 
                         [0, 1, 4, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24, 29, 31], 
                         cube=cube_dict['additional'])

        self.additional_subweapon_option_prob_first.append(1 - sum(self.additional_subweapon_option_prob_first))
        self.additional_subweapon_option_prob_second.append(1 - sum(self.additional_subweapon_option_prob_second))
        self.additional_subweapon_option_prob_third.append(1 - sum(self.additional_subweapon_option_prob_third))

        # 엠블럼
        self.additional_emblem_option_first: list = ['p_power12', 'm_power12', 'critical12', 
                                                     'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                     'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                     'Def5', 'etc']
        self.additional_emblem_option_second: list = ['p_power12', 'm_power12', 'p_power9', 'm_power9', 'critical12', 'critical9',
                                                      'str12', 'dex12', 'int12', 'luk12', 'damage12', 'all9',
                                                      'str9', 'dex9', 'int9', 'luk9', 'damage9', 'all6',
                                                      'Str+2', 'Dex+2', 'Int+2', 'Luk+2', 'Phy+1', 'Mag+1',
                                                      'Str+1', 'Dex+1', 'Int+1', 'Luk+1',
                                                      'Def5', 'Def4', 'etc']
        self.additional_emblem_option_third: list = self.additional_emblem_option_second[:]
        self.additional_emblem_option_weight_first: list = [1, 1, 1, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 3.5]
        self.additional_emblem_option_weight_second: list = [1, 1, 1, 1.5, 1.5, 1.5, 1.5, 0.5, 1, 1, 1, 1, 1, 0.5, 6]
        self.additional_emblem_option_weight_third: list = self.additional_emblem_option_weight_second[:]
        self.additional_emblem_option_prob_first: list = []
        self.additional_emblem_option_prob_second: list = []
        self.additional_emblem_option_prob_third: list = []

        self.createTable(self.additional_emblem_option_first, self.additional_emblem_option_second, self.additional_emblem_option_third,
                         self.additional_emblem_option_weight_first, self.additional_emblem_option_weight_second, self.additional_emblem_option_weight_third,
                         self.additional_emblem_option_prob_first, self.additional_emblem_option_prob_second, self.additional_emblem_option_prob_third,
                         [2, 3, 5, 12, 13, 14, 15, 16, 17, 24, 25, 26, 27, 29], 
                         [0, 1, 4, 6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23, 28], 
                         cube=cube_dict['additional'])

        self.additional_emblem_option_prob_first.append(1 - sum(self.additional_emblem_option_prob_first))
        self.additional_emblem_option_prob_second.append(1 - sum(self.additional_emblem_option_prob_second))
        self.additional_emblem_option_prob_third.append(1 - sum(self.additional_emblem_option_prob_third))

    # 레드 큐브(이전)
    def getWeapon(self) -> List[list]:
        '''
            무기 - 레드 큐브(이전)
        '''
        return [self.weapon_option_first, self.weapon_option_second, self.weapon_option_third, 
                self.weapon_option_prob_first, self.weapon_option_prob_second, self.weapon_option_prob_third]
    
    def getSubweapon(self) -> List[list]:
        '''
            보조무기 - 레드 큐브(이전)
        '''
        return [self.subweapon_option_first, self.subweapon_option_second, self.subweapon_option_third, 
                self.subweapon_option_prob_first, self.subweapon_option_prob_second, self.subweapon_option_prob_third]

    def getEmblem(self) -> List[list]:
        '''
            엠블럼 - 레드 큐브(이전)
        '''
        return [self.emblem_option_first, self.emblem_option_second, self.emblem_option_third,
                self.emblem_option_prob_first, self.emblem_option_prob_second, self.emblem_option_prob_third]

    # 블랙 큐브(이전)
    def getBlackweapon(self) -> List[list]:
        '''
            무기 - 블랙 큐브(이전)
        '''
        return [self.weapon_black_option_first, self.weapon_black_option_second, self.weapon_black_option_third, 
                self.weapon_black_option_prob_first, self.weapon_black_option_prob_second, self.weapon_black_option_prob_third]
    
    def getBlacksubweapon(self) -> List[list]:
        '''
            보조무기 - 블랙 큐브(이전)
        '''
        return [self.subweapon_black_option_first, self.subweapon_black_option_second, self.subweapon_black_option_third, 
                self.subweapon_black_option_prob_first, self.subweapon_black_option_prob_second, self.subweapon_black_option_prob_third]

    def getBlackemblem(self) -> List[list]:
        '''
            엠블럼 - 블랙 큐브(이전)
        '''
        return [self.emblem_black_option_first, self.emblem_black_option_second, self.emblem_black_option_third,
                self.emblem_black_option_prob_first, self.emblem_black_option_prob_second, self.emblem_black_option_prob_third]

    # 레드 큐브(이후)

    # 븡랙 큐브(이후)

    # 에디셔널 큐브
    def getAdditionalweapon(self) -> List[list]:
        '''
            무기 - 에디셔널 큐브
        '''
        return [self.additional_weapon_option_first, self.additional_weapon_option_second, self.additional_weapon_option_third,
                self.additional_weapon_option_prob_first, self.additional_weapon_option_prob_second, self.additional_weapon_option_prob_third]
    
    def getAdditionalsubweapon(self) -> List[list]:
        '''
            보조무기 - 에디셔널 큐브
        '''
        return [self.additional_subweapon_option_first, self.additional_subweapon_option_second, self.additional_subweapon_option_third,
                self.additional_subweapon_option_prob_first, self.additional_subweapon_option_prob_second, self.additional_subweapon_option_prob_third]
                
    def getAdditionalemblem(self) -> List[list]:
        '''
            엠블럼 - 에디셔널 큐브
        '''
        return [self.additional_emblem_option_first, self.additional_emblem_option_second, self.additional_emblem_option_third,
                self.additional_emblem_option_prob_first, self.additional_emblem_option_prob_second, self.additional_emblem_option_prob_third]