'''
    Coded by Cho_bo

    weapon.py
        - 잠재능력 표본 추출

    2021-08-09 ~
'''
from multiprocessing import Array, Manager, Process, current_process, cpu_count
from typing import List
from util import concat_all, exit_func, get_time, NotDefinedNumberError

import csv, math, random
import os, sys
import potentialtable

def counting_option(option_dict: dict, option_count, first_option: str, second_option: str, third_option: str, print_log: bool) -> None:
    '''
        경우의 수를 전부 입력하긴 코드가 더러워져서, 따로 함수를 빼두었다.
        공격력은 1, 마력은 10, 보공은 100, 방무는 1000단위에서 dict를 통해 count 진행.

        ex)
            1101 = 방무 1줄, 보공 1줄, 공격력 1줄
            12 = 마력 1줄, 공격력 2줄

        input
            option_dict : simulation - option_dict
            option_count : 3줄 유효 카운트
            first_option : 첫번째 옵션
            second_option : 두번째 옵션
            third_option : 세번째 옵션
            print_log: 로그 출력 / 미출력

        output
            SynchronizedArray(option_count) 에 카운트된다.
    '''
    # 순서대로 공격력, 마력, 보공, 방무
    option_check: list = [0 for _ in range(4)]
    op: tuple = (option_dict[first_option], option_dict[second_option], option_dict[third_option])
    mapping_option: dict = {1: 0, 2: 1,
                            3: 0, 4: 1,
                            5: 2, 6: 2, 7: 2, 8: 2, 
                            9: 3, 10: 3, 11: 3}

    # 뾰공이 존재하지 않는 보보공
    mapping_count: dict = {3: 0, 102: 1, 1002: 2, 201: 3, 1101: 4, 2001: 5, 
                           30: 6, 120: 7, 1020: 8, 210: 9, 1110: 10, 2010: 11,
                           1200: 12, 2100: 13}

    # 뾰공이 존재할 때...
    shit_mapping_count: dict = {102: 14, 201: 15, 1101: 16,
                                120: 17, 210: 18, 1110: 19,
                                1200: 20, 2100: 21}

    # 뾰공 리스트
    shit_boss_list_first30: list = [('boss30', 'p_power9', 'p_power9'), ('boss30', 'p_power9', 'boss30'), ('boss30', 'p_power9', 'def30'),
                                    ('boss30', 'm_power9', 'm_power9'), ('boss30', 'm_power9', 'boss30'), ('boss30', 'm_power9', 'def30'),
                                    ('boss30', 'boss30', 'def30')]

    # 뾰공이 섞였어도 이탈이라 아닌 리스트
    not_shit_boss_list_20: list = [('boss40', 'p_power12', 'boss20'), ('boss35', 'p_power12', 'boss20'),
                                   ('def40', 'boss40', 'boss20'), ('p_power12', 'p_power12', 'boss20'),
                                   ('boss40', 'def40', 'boss20'), ('boss40', 'def35', 'boss20')]

    # 뾰공이 있는가? 없는가?
    shit_boss_option = False
    for i in range(len(op)):
        if op[i] not in [12, 13]:
            option_check[mapping_option[op[i]]] += 1
            if i == 0 and op[i] == 6:
                if (first_option, second_option, third_option) in shit_boss_list_first30 or (first_option, third_option, second_option) in shit_boss_list_first30:
                    shit_boss_option = True
            
            elif i in [1, 2] and op[i] == 5:
                if (first_option, second_option, third_option) not in not_shit_boss_list_20 and (first_option, third_option, second_option) not in not_shit_boss_list_20:
                    shit_boss_option = True

    option_sum: int = 0
    if sum(option_check) == 3:
        for i in range(4):
            option_sum += option_check[i] * int(math.pow(10, i))
    
        if option_sum not in [12, 21, 111, 1011]:
            option_count[mapping_count[option_sum]] += 1
            if shit_boss_option:
                if print_log:
                    print(f"Process PID({current_process().pid}) -> Log (include shit_boss_option) : ({first_option}, {second_option}, {third_option})")
                option_count[shit_mapping_count[option_sum]] += 1

    return

def counting_option_additional(option_dict: dict, option_count, first_option: str, second_option: str, third_option: str, print_log: bool) -> None:
    '''
        (에디셔널 전용)
        경우의 수를 전부 입력하긴 코드가 더러워져서, 따로 함수를 빼두었다.
        공격력은 1, 마력은 10, 보공은 100, 방무는 1000단위에서 dict를 통해 count 진행.

        이 역시 원래 counting_option과는 다르게, 유효 옵션의 경우의 수가 많으므로 각각의 케이스를 전부 string식으로 처리하기 위해 빼두었다.

        여기서의 약자는 다음과 같다. (사전 순서)
            a : all9, all6
            b : boss18, boss12
            c : critical12, critical9
            C : cridamage1
            d : damage12, damage9,
            D : def5, def4
            e : etc
            i : int12, int9
            I : int+2, int+1
            l : luk12, luk9
            L : luk+2, luk+1
            m : m_power12, m_power9
            M : mag+1
            p : p_power12, p_power9
            P : phy+1
            s : str12, str9
            S : str+2, str+1
            x : dex12, dex9
            X : dex+2, dex+1

        input
            option_dict : simulation_additional - option_dict
            option_count : 3줄 유효 카운트
            first_option : 첫번째 옵션
            second_option : 두번째 옵션
            third_option : 세번째 옵션
            print_log: 로그 출력 / 미출력

        output
            SynchronizedArray(option_count) 에 카운트된다.
    '''

    def prefix_append(option_dict: dict, target: str) -> str:
        '''
            내장 함수, 접두사를 붙여준다.
        '''
        if option_dict[target] in [9, 15]:
            return 'x' + target
        elif option_dict[target] in [21, 27]:
            return 'X' + target
        else:
            return target

    # 순서대로 공격력, 마력, 보공
    option_check: list = [0 for _ in range(3)]

    # 에디셔널 옵션의 종류
    # 일단 공, 마 2줄 이상인지 체크하고, 이후에 사용됨.
            
    # 에디 기준 (main 참조)
    # 공공잡, 공공크, 공공크뎀, 공공힘, 공공덱, 공공럭, 공공뎀, 공공올, 공공공, 공공공+1, 공공방, 공공보
    # 마마잡, 마마크, 마마크뎀, 마마인, 마마뎀, 마마마, 마마마+1, 마마방, 마마보
    # 보보공, 보보마
    mapping_option: dict = {# 'ppe': 0, 'pep': 0,
                            'ppc': 1, 'pcp': 1, 'cpp': 1,
                            'ppC': 2, 'pCp': 2,
                            'pps': 3, 'psp': 3, 'spp': 3, 'ppS': 3, 'pSp': 3, 'Spp': 3,
                            'ppx': 4, 'pxp': 4, 'xpp': 4, 'ppX': 4, 'pXp': 4, 'Xpp': 4,
                            'ppl': 5, 'plp': 5, 'lpp': 5, 'ppL': 5, 'pLp': 5, 'Lpp': 5,
                            'ppd': 6, 'pdp': 6, 'dpp': 6,
                            'ppa': 7, 'pap': 7, 'app': 7,
                            'ppp': 8,
                            'ppP': 9, 'pPp': 9, 'Ppp': 9,
                            'ppD': 10, 'pDp': 10,
                            'ppb': 11, 'pbp': 11, 'bpp': 11,
                            # 'mme': 12, 'mem: 12,
                            'mmc': 13, 'mcm': 13, 'cmm': 13,
                            'mmC': 14, 'mCm': 14,
                            'mmi': 15, 'mim': 15, 'imm': 15, 'mmI': 15, 'mIm': 15, 'Imm': 15,
                            'mmd': 16, 'mdm': 16, 'dmm': 16,
                            'mma': 17, 'mam': 17, 'amm': 17,
                            'mmm': 18,
                            'mmM': 19, 'mMm': 19, 'Mmm': 19,
                            'mmD': 20, 'mDm': 20,
                            'mmb': 21, 'mbm': 21, 'bmm': 21,
                            'bbp': 22, 'bpb': 22, 'pbb': 22,
                            'bbm': 23, 'bmb': 23, 'mbb': 23}

    mapping_check: dict = {'p': 0, 'm': 1, 'b': 2}
    option_string: str = []
    
    addprefix_first_option = prefix_append(option_dict, first_option)
    addprefix_second_option = prefix_append(option_dict, second_option)
    addprefix_third_option = prefix_append(option_dict, third_option)

    for i in [addprefix_first_option, addprefix_second_option, addprefix_third_option]:
        if i[0] in mapping_check:
            option_check[mapping_check[i[0]]] += 1
        option_string.append(i[0])
    
    option_string = concat_all(*option_string)
    if option_check[0] >= 2 or option_check[1] >= 2 or (option_check[2] == 2 and sum(option_check) == 3):
        if option_check[0] >= 2:
            option_count[0] += 1
        elif option_check[1] >= 2:
            option_count[12] += 1

        if option_string in mapping_option:
            if print_log:
                print(f"Process PID({current_process().pid}) -> Log : ({first_option}, {second_option}, {third_option}), keyword : ({option_string})")
            option_count[mapping_option[option_string]] += 1

    return

def simulation(sample_list, option_count, collision_count, option: list, option_prob: list, start: int, end: int, print_log: bool) -> None:
    '''
        멀티코어로 돌아가는 함수
        
        input
            sample_list : 결과를 전부 append하는 manager - array
            option_count : 3줄 유효 카운트
            option : 선택한 무기 타입의 옵션 종류
            option_prob : 선택한 무기 타입의 옵션 확률
            start: 반복의 시작
            end: 반복의 끝
            print_log: 로그 출력 / 미출력

        output
            sample_list에 전부 append됨.
    '''
    # 피격시는 12이다. (보조무기용)
    option_dict: dict = {'p_power12' : 1, 'm_power12' : 2, 'p_power9' : 3, 'm_power9' : 4,
                         'boss20'    : 5, 'boss30'    : 6, 'boss35'   : 7, 'boss40'   : 8,
                         'def30'     : 9, 'def35'     : 10,'def40'    : 11,
                         'attacked'  : 12,'etc'       : 13}
    print(f"Process PID({current_process().pid}) : Work (iteration number {start} to {end}) is allocated.")
    for _ in range(start, end):
        first_option: str = random.choices(option[0], weights=option_prob[0])[0]
        second_option: str = random.choices(option[1], weights=option_prob[1])[0]

        double_boss: bool = False
        double_def: bool = False
        double_attacked: bool = False
        if 5 <= option_dict[first_option] <= 8 and 5 <= option_dict[second_option] <= 8:
            double_boss = True
        if 9 <= option_dict[first_option] <= 11 and 9 <= option_dict[second_option] <= 11:
            double_def = True
        if option_dict[first_option] == 12 and option_dict[second_option] == 12:
            double_attacked = True

        while True:
            third_option: str = random.choices(option[2], weights=option_prob[2])[0]
            if double_boss and 5 <= option_dict[third_option] <= 8:
                collision_count[0] += 1
                continue
            if double_def and 9 <= option_dict[third_option] <= 11:
                collision_count[1] += 1
                continue
            if double_attacked and option_dict[third_option] == 12:
                collision_count[2] += 1
                continue

            break

        sample_list.append([first_option, second_option, third_option])
        counting_option(option_dict, option_count, first_option, second_option, third_option, print_log)
        
    print(f"Process PID({current_process().pid}) : work done, iteration count : {end - start}")
    return

def simulation_additional(sample_list, option_count, collision_count, option: list, option_prob: list, start: int, end: int, print_log: bool) -> None:
    '''
        (에디셔널 전용)
        멀티코어로 돌아가는 함수
        원래 시뮬과 합치기엔 option_dict 자체가 달라지므로 따로 분리해두었다.
        
        input
            sample_list : 결과를 전부 append하는 manager - array
            option_count : 3줄 유효 카운트
            option : 선택한 무기 타입의 옵션 종류
            option_prob : 선택한 무기 타입의 옵션 확률
            start: 반복의 시작
            end: 반복의 끝
            print_log: 로그 출력 / 미출력

        output
            sample_list에 전부 append됨.
    '''

    # 크리 데미지는 7이다. (보조무기용)
    option_dict: dict = {'p_power12': 1, 'm_power12': 2, 'p_power9': 3, 'm_power9': 4, 'critical12': 5, 'critical9': 6, 'Cridamage1' : 7,
                         'str12'    : 8, 'dex12'    : 9, 'int12'  : 10, 'luk12'  : 11, 'damage12' : 12, 'all9'     : 13,
                         'str9'    : 14, 'dex9'    : 15, 'int9'   : 16, 'luk9'   : 17, 'damage9'  : 18, 'all6'     : 19,
                         'Str+2'   : 20, 'Dex+2'   : 21, 'Int+2'  : 22, 'Luk+2'  : 23, 'Phy+1'    : 24, 'Mag+1'    : 25,
                         'Str+1'   : 26, 'Dex+1'   : 27, 'Int+1'  : 28, 'Luk+1'  : 29,
                         'Def5'    : 30, 'Def4'    : 31, 'boss18' : 32, 'boss12' : 33, 'etc'      : 34}
    print(f"Process PID({current_process().pid}) : Work (iteration number {start} to {end}) is allocated.")
    for _ in range(start, end):
        first_option: str = random.choices(option[0], weights=option_prob[0])[0]
        second_option: str = random.choices(option[1], weights=option_prob[1])[0]

        double_boss: bool = False
        double_def: bool = False
        if 32 <= option_dict[first_option] <= 33 and 32 <= option_dict[second_option] <= 33:
            double_boss = True
        if 30 <= option_dict[first_option] <= 31 and 30 <= option_dict[second_option] <= 31:
            double_def = True

        while True:
            third_option: str = random.choices(option[2], weights=option_prob[2])[0]
            if double_boss and 32 <= option_dict[third_option] <= 33:
                collision_count[0] += 1
                continue
            if double_def and 30 <= option_dict[third_option] <= 31:
                collision_count[1] += 1
                continue

            break

        sample_list.append([first_option, second_option, third_option])
        counting_option_additional(option_dict, option_count, first_option, second_option, third_option, print_log)
        
    print(f"Process PID({current_process().pid}) : work done, iteration count : {end - start}")
    return

def main() -> None:
    '''
        Main func, 모든 무기 종류에 대한 옵션 종류, 확률 초기화
    '''
    # potentialtable.py 참조
    get_table = potentialtable.table()

    # 아이템 타입 dict
    item_type: dict = {1: 'Weapon', 2: 'SubWeapon', 3: 'Emblem'}

    # 아이템 타입 dict
    cube_type: dict = {1: 'Red Cube', 2: 'Black Cube', 3: 'Additional Cube'}

    # 테이블 타입 dict
    table_type: dict = {1: 'old', 2: 'new'}

    # 잠재능력 테이블 dict
    # tuple key는 (cube_input, table_input, select)
    set_potential_table: dict = {(1, 1, 1) : get_table.getWeapon(), (1, 1, 2) : get_table.getSubweapon(), (1, 1, 3) : get_table.getEmblem(),
                                 (2, 1, 1) : get_table.getBlackweapon(), (2, 1, 2) : get_table.getBlacksubweapon(), (2, 1, 3) : get_table.getBlackemblem(),
                                 (1, 2, 1) : get_table.getNewweapon(), (1, 2, 2) : get_table.getNewsubweapon(), (1, 2, 3) : get_table.getNewemblem(),
                                 (2, 2, 1) : get_table.getNewblackweapon(), (2, 2, 2) : get_table.getNewblacksubweapon(), (2, 2, 3) : get_table.getNewblackemblem(),
                                 (3, 1, 1) : get_table.getAdditionalweapon(), (3, 1, 2) : get_table.getAdditionalsubweapon(), (3, 1, 3) : get_table.getAdditionalemblem()}
    
    # 시뮬레이션 선택
    set_simulation: dict = {1: simulation, 2: simulation_additional}
    
    while True:
        try:
            # 선택한 조건에 따른 옵션 종류와 확률 저장
            select_option: list = []
            select_option_prob: list = []
            
            # 윗잠 기준
            # 공공공, 공공보, 공공방, 공보보, 공보방, 공방방, 마마마, 마마보, 마마방, 마보보, 마보방, 마방방, 보보방, 보방방
            # index 14부턴 뾰공이 섞인 공공보, 공보보, 공보방, 마마보, 마보보, 마보방, 보보방, 보방방
            
            # 에디 기준
            # 공공잡, 공공크, 공공크뎀, 공공힘, 공공덱, 공공럭, 공공뎀, 공공올, 공공공, 공공공+1, 공공방, 공공보
            # 마마잡, 마마크, 마마크뎀, 마마인, 마마뎀, 마마마, 마마마+1, 마마방, 마마보
            # 보보공, 보보마
            option_count = Array('d', [0 for _ in range(24)])

            # 보보보, 방방방, 피피피
            collision_count = Array('d', [0 for _ in range(3)])

            print("Select\n"
                  "---------------------------\n"
                  "1. Weapon\n"
                  "2. SubWeapon\n"
                  "3. Emblem\n"
                  "4. Exit")
            select: int = int(sys.stdin.readline().strip())
            if select == 4:
                exit_func()

            print("\nSet Simulation type ( 1: default, 2: additional )")
            potential_input: int = int(sys.stdin.readline().strip())

            # select나 potential_type이 지정된 숫자가 아니면 exception
            if select not in [i for i in range(1, 5)] or potential_input not in [1, 2]:
                raise NotDefinedNumberError

            # 3은 에디셔널 큐브, 에디는 기본적으로 table_type이 1
            cube_input: int = 3
            table_input: int = 1

            # potential_input이 1이면 윗잠이므로, 세부 값 결정
            if potential_input == 1:
                print("\nSet Cube type ( 1: red, 2: black )")
                cube_input = int(sys.stdin.readline().strip())

                print("\nSet Cube Table ( 1: old( ~ 2021.08.11 ), 2: new( 2021.08.12 ~ ) )")
                table_input = int(sys.stdin.readline().strip())

            # cube_type, table_type exception check
            if cube_input not in [1, 2, 3] and table_input not in [1, 2]:
                raise NotDefinedNumberError

            # 결정된 확률 테이블
            set_table : List[list] = set_potential_table[(cube_input, table_input, select)]
            
            for option_table in set_table[:3]:
                select_option.append(option_table)

            for option_prob in set_table[-3:]:
                select_option_prob.append(option_prob)

            print("\nType sample size( >= 1 )")
            count: int = int(sys.stdin.readline().strip())
            
            # 확률 체크 용 print 디버깅
            print(select_option_prob)
            print(select_option)
            print("\nPrint Log?\n"
                  "---------------------------\n"
                  "0: no, 1: yes")
            print_log: bool = True if int(sys.stdin.readline().strip()) else False

            # count exception check
            if count <= 0:
                raise NotDefinedNumberError
            
            with Manager() as manager:
                # multiprocessing list, Save all samples' information
                sample_list = manager.list()
                
                # process list
                processes: list = []
                num_process: int = cpu_count()
                
                iter_start: int = 0
                iter_end: int = round(count / num_process)

                try:
                    print("\nPlease Wait...\n")
                    for i in range(num_process):
                        p = Process(target = set_simulation[potential_input], args=(sample_list, option_count, collision_count, 
                                                                                    select_option, select_option_prob, 
                                                                                    iter_start, iter_end, print_log))
                        p.start()
                        processes.append(p)
                        iter_start = iter_end
                        iter_end = round((i + 2) * count / num_process)
                    
                    for p in processes:
                        p.join()
                        p.close()
                    
                    nowtime: str = get_time()
                    resultmsg: str = ''

                    if cube_input != 3:
                        if select != 3:
                            resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                                   f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n확률 테이블 : {table_type[table_input]}\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"옵션 종류\n",
                                                   f"공공공 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%   ",
                                                   f"공공보 : {int(option_count[1])}, {round(option_count[1] * 100 / count, 3)}%   ",
                                                   f"공공방 : {int(option_count[2])}, {round(option_count[2] * 100 / count, 3)}%\n",
                                                   f"공보보 : {int(option_count[3])}, {round(option_count[3] * 100 / count, 3)}%   ",
                                                   f"공보방 : {int(option_count[4])}, {round(option_count[4] * 100 / count, 3)}%   ",
                                                   f"공방방 : {int(option_count[5])}, {round(option_count[5] * 100 / count, 3)}%\n",
                                                   f"마마마 : {int(option_count[6])}, {round(option_count[6] * 100 / count, 3)}%   ",
                                                   f"마마보 : {int(option_count[7])}, {round(option_count[7] * 100 / count, 3)}%   ",
                                                   f"마마방 : {int(option_count[8])}, {round(option_count[8] * 100 / count, 3)}%\n",
                                                   f"마보보 : {int(option_count[9])}, {round(option_count[9] * 100 / count, 3)}%   ",
                                                   f"마보방 : {int(option_count[10])}, {round(option_count[10] * 100 / count, 3)}%   ",
                                                   f"마방방 : {int(option_count[11])}, {round(option_count[11] * 100 / count, 3)}%\n",
                                                   f"보보방 : {int(option_count[12])}, {round(option_count[12] * 100 / count, 3)}%   ",
                                                   f"보방방 : {int(option_count[13])}, {round(option_count[13] * 100 / count, 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"그중에 뾰공은?\n",
                                                   f"공공보 : {int(option_count[14])}, {round(option_count[14] * 100 / option_count[1], 3)}%   ",
                                                   f"공보보 : {int(option_count[15])}, {round(option_count[15] * 100 / option_count[3], 3)}%   ",
                                                   f"공보방 : {int(option_count[16])}, {round(option_count[16] * 100 / option_count[4], 3)}%\n",
                                                   f"마마보 : {int(option_count[17])}, {round(option_count[17] * 100 / option_count[7], 3)}%   ",
                                                   f"마보보 : {int(option_count[18])}, {round(option_count[18] * 100 / option_count[9], 3)}%   ",
                                                   f"마보방 : {int(option_count[19])}, {round(option_count[19] * 100 / option_count[10], 3)}%\n",
                                                   f"보보방 : {int(option_count[20])}, {round(option_count[20] * 100 / option_count[12], 3)}%   ",
                                                   f"보방방 : {int(option_count[21])}, {round(option_count[21] * 100 / option_count[13], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"번외\n",
                                                   f"보보보 : {int(collision_count[0])}, 방방방 : {int(collision_count[1])}\n",
                                                   f"--------------------------------------------------------------------")
                        else:
                            resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                                   f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n확률 테이블 : {table_type[table_input]}\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"옵션 종류\n",
                                                   f"공공공 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%   ",
                                                   f"공공방 : {int(option_count[2])}, {round(option_count[2] * 100 / count, 3)}%   ",
                                                   f"공방방 : {int(option_count[5])}, {round(option_count[5] * 100 / count, 3)}%\n",
                                                   f"마마마 : {int(option_count[6])}, {round(option_count[6] * 100 / count, 3)}%   ",
                                                   f"마마방 : {int(option_count[8])}, {round(option_count[8] * 100 / count, 3)}%   ",
                                                   f"마방방 : {int(option_count[11])}, {round(option_count[11] * 100 / count, 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"번외\n",
                                                   f"방방방 : {int(collision_count[1])}\n",
                                                   f"--------------------------------------------------------------------")

                    else:
                        if select == 1:
                            resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                                   f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"옵션 종류\n",
                                                   f"공 2줄 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%\n\n",
                                                   f"공 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"공공크 : {int(option_count[1])}, {round(option_count[1] * 100 / option_count[0], 3)}%   ",
                                                   f"공공힘 : {int(option_count[3])}, {round(option_count[3] * 100 / option_count[0], 3)}%   ",
                                                   f"공공덱 : {int(option_count[4])}, {round(option_count[4] * 100 / option_count[0], 3)}%\n",
                                                   f"공공럭 : {int(option_count[5])}, {round(option_count[5] * 100 / option_count[0], 3)}%   ",
                                                   f"공공뎀 : {int(option_count[6])}, {round(option_count[6] * 100 / option_count[0], 3)}%   ",
                                                   f"공공올 : {int(option_count[7])}, {round(option_count[7] * 100 / option_count[0], 3)}%\n",
                                                   f"공공공 : {int(option_count[8])}, {round(option_count[8] * 100 / option_count[0], 3)}%   ",
                                                   f"공공공+1 : {int(option_count[9])}, {round(option_count[9] * 100 / option_count[0], 3)}%\n",
                                                   f"공공방 : {int(option_count[10])}, {round(option_count[10] * 100 / option_count[0], 3)}%   ",
                                                   f"공공보 : {int(option_count[11])}, {round(option_count[11] * 100 / option_count[0], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"마 2줄 : {int(option_count[12])}, {round(option_count[12] * 100 / count, 3)}%\n\n",
                                                   f"마 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"마마크 : {int(option_count[13])}, {round(option_count[13] * 100 / option_count[12], 3)}%   ",
                                                   f"마마인 : {int(option_count[15])}, {round(option_count[15] * 100 / option_count[12], 3)}%   ",
                                                   f"마마뎀 : {int(option_count[16])}, {round(option_count[16] * 100 / option_count[12], 3)}%   ",
                                                   f"마마올 : {int(option_count[17])}, {round(option_count[17] * 100 / option_count[12], 3)}%\n",
                                                   f"마마마 : {int(option_count[18])}, {round(option_count[18] * 100 / option_count[12], 3)}%   ",
                                                   f"마마마+1 : {int(option_count[19])}, {round(option_count[19] * 100 / option_count[12], 3)}%\n",
                                                   f"마마방 : {int(option_count[20])}, {round(option_count[20] * 100 / option_count[12], 3)}%   ",
                                                   f"마마보 : {int(option_count[21])}, {round(option_count[21] * 100 / option_count[12], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"보공 2줄 포함 3유효\n",
                                                   f"보보공 : {int(option_count[22])}, {round(option_count[22] * 100 / count, 3)}%   ",
                                                   f"보보마 : {int(option_count[23])}, {round(option_count[23] * 100 / count, 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"번외\n",
                                                   f"보보보 : {int(collision_count[0])}, 방방방 : {int(collision_count[1])}\n",
                                                   f"--------------------------------------------------------------------")
                        elif select == 2:
                            resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                                   f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"옵션 종류\n",
                                                   f"공 2줄 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%\n\n",
                                                   f"공 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"공공크 : {int(option_count[1])}, {round(option_count[1] * 100 / option_count[0], 3)}%   ",
                                                   f"공공크뎀 : {int(option_count[2])}, {round(option_count[2] * 100 / option_count[0], 3)}%   ",
                                                   f"공공힘 : {int(option_count[3])}, {round(option_count[3] * 100 / option_count[0], 3)}%\n",
                                                   f"공공덱 : {int(option_count[4])}, {round(option_count[4] * 100 / option_count[0], 3)}%   ",
                                                   f"공공럭 : {int(option_count[5])}, {round(option_count[5] * 100 / option_count[0], 3)}%   ",
                                                   f"공공뎀 : {int(option_count[6])}, {round(option_count[6] * 100 / option_count[0], 3)}%\n",
                                                   f"공공올 : {int(option_count[7])}, {round(option_count[7] * 100 / option_count[0], 3)}%   ",
                                                   f"공공공 : {int(option_count[8])}, {round(option_count[8] * 100 / option_count[0], 3)}%   ",
                                                   f"공공공+1 : {int(option_count[9])}, {round(option_count[9] * 100 / option_count[0], 3)}%\n",
                                                   f"공공방 : {int(option_count[10])}, {round(option_count[10] * 100 / option_count[0], 3)}%   ",
                                                   f"공공보 : {int(option_count[11])}, {round(option_count[11] * 100 / option_count[0], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"마 2줄 : {int(option_count[12])}, {round(option_count[12] * 100 / count, 3)}%\n\n",
                                                   f"마 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"마마크 : {int(option_count[13])}, {round(option_count[13] * 100 / option_count[12], 3)}%   ",
                                                   f"마마크뎀 : {int(option_count[14])}, {round(option_count[14] * 100 / option_count[12], 3)}%   ",
                                                   f"마마인 : {int(option_count[15])}, {round(option_count[15] * 100 / option_count[12], 3)}%\n",
                                                   f"마마뎀 : {int(option_count[16])}, {round(option_count[16] * 100 / option_count[12], 3)}%   ",
                                                   f"마마올 : {int(option_count[17])}, {round(option_count[17] * 100 / option_count[12], 3)}%   ",
                                                   f"마마마 : {int(option_count[18])}, {round(option_count[18] * 100 / option_count[12], 3)}%\n",
                                                   f"마마마+1 : {int(option_count[19])}, {round(option_count[19] * 100 / option_count[12], 3)}%   ",
                                                   f"마마방 : {int(option_count[20])}, {round(option_count[20] * 100 / option_count[12], 3)}%   ",
                                                   f"마마보 : {int(option_count[21])}, {round(option_count[21] * 100 / option_count[12], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"보공 2줄 포함 3유효\n",
                                                   f"보보공 : {int(option_count[22])}, {round(option_count[22] * 100 / count, 3)}%   ",
                                                   f"보보마 : {int(option_count[23])}, {round(option_count[23] * 100 / count, 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"번외\n",
                                                   f"보보보 : {int(collision_count[0])}, 방방방 : {int(collision_count[1])}\n",
                                                   f"--------------------------------------------------------------------")
                        else:
                            resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                                   f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"옵션 종류\n",
                                                   f"공 2줄 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%\n\n",
                                                   f"공 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"공공크 : {int(option_count[1])}, {round(option_count[1] * 100 / option_count[0], 3)}%   ",
                                                   f"공공힘 : {int(option_count[3])}, {round(option_count[3] * 100 / option_count[0], 3)}%   ",
                                                   f"공공덱 : {int(option_count[4])}, {round(option_count[4] * 100 / option_count[0], 3)}%\n",
                                                   f"공공럭 : {int(option_count[5])}, {round(option_count[5] * 100 / option_count[0], 3)}%   ",
                                                   f"공공뎀 : {int(option_count[6])}, {round(option_count[6] * 100 / option_count[0], 3)}%   ",
                                                   f"공공올 : {int(option_count[7])}, {round(option_count[7] * 100 / option_count[0], 3)}%\n",
                                                   f"공공공 : {int(option_count[8])}, {round(option_count[8] * 100 / option_count[0], 3)}%   ",
                                                   f"공공공+1 : {int(option_count[9])}, {round(option_count[9] * 100 / option_count[0], 3)}%   ",
                                                   f"공공방 : {int(option_count[10])}, {round(option_count[10] * 100 / option_count[0], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"마 2줄 : {int(option_count[12])}, {round(option_count[12] * 100 / count, 3)}%\n\n",
                                                   f"마 2줄을 포함한 3줄 유효 케이스들\n",
                                                   f"마마크 : {int(option_count[13])}, {round(option_count[13] * 100 / option_count[12], 3)}%   ",
                                                   f"마마인 : {int(option_count[15])}, {round(option_count[15] * 100 / option_count[12], 3)}%   ",
                                                   f"마마뎀 : {int(option_count[16])}, {round(option_count[16] * 100 / option_count[12], 3)}%   ",
                                                   f"마마올 : {int(option_count[17])}, {round(option_count[17] * 100 / option_count[12], 3)}%\n",
                                                   f"마마마 : {int(option_count[18])}, {round(option_count[18] * 100 / option_count[12], 3)}%   ",
                                                   f"마마마+1 : {int(option_count[19])}, {round(option_count[19] * 100 / option_count[12], 3)}%   ",
                                                   f"마마방 : {int(option_count[20])}, {round(option_count[20] * 100 / option_count[12], 3)}%\n",
                                                   f"--------------------------------------------------------------------\n",
                                                   f"번외\n",
                                                   f"방방방 : {int(collision_count[1])}\n",
                                                   f"--------------------------------------------------------------------")

                    csvname: str = concat_all(nowtime, "_", item_type[select], ".csv")
                    txtname: str = concat_all(nowtime, "_", item_type[select], ".txt")

                    with open(csvname, "w", newline="") as savefile:
                        csvwriter = csv.writer(savefile)
                        csvindex = 1

                        # Data Format
                        # In case of boolean, 0 : Disable, 1 : Enable
                        fields = ['', 
                                'first_option', 'second_option', 'third_option']
                        csvwriter.writerow(fields)

                        for row in sample_list:
                            csvwriter.writerow([csvindex, *row])
                            csvindex += 1

                        print(f"\nExporting to csv is completed.\n"
                            f"------------------------------------\n"
                            f"Filename : {csvname}\nTotal number of samples: {csvindex-1}\nFilesize : {savefile.seek(0, os.SEEK_END)} bytes\n")

                        savefile.close()
                    with open(txtname, "w", newline="") as savefile:
                        savefile.write(resultmsg)

                        print(f"\nExporting to txt is completed.\n"
                            f"------------------------------------\n"
                            f"Filename : {txtname}\nFilesize : {savefile.seek(0, os.SEEK_END)} bytes\n")

                        savefile.close()

                except Exception as e:
                    print(f"\nException Alerted. {e}\n")
                    exit_func()

        except Exception as e:
            print(f"\nException Alerted. {e}\n")
            exit_func()

if __name__ == '__main__':
    main()