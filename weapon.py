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
            None
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
        
        counting_option(option_dict, option_count, first_option, second_option, third_option, print_log)
        sample_list.append([first_option, second_option, third_option])
        
    print(f"Process PID({current_process().pid}) : work done, iteration count : {end - start}")
    return

def main() -> None:
    '''
        Main func, 모든 무기 종류에 대한 옵션 종류, 확률 초기화
    '''
    # potentialtable.py 참조
    get_table = potentialtable.table()

    # 선택한 조건에 따른 옵션 종류와 확률 저장
    select_option: list = []
    select_option_prob: list = []

    # 공공공, 공공보, 공공방, 공보보, 공보방, 공방방, 마마마, 마마보, 마마방, 마보보, 마보방, 마방방, 보보방, 보방방
    # index 14부턴 뾰공이 섞인 공공보, 공보보, 공보방, 마마보, 마보보, 마보방, 보보방, 보방방
    '''
        ★에디는 어떤 걸 추가해야 할 지 추후 고려 예정.
    '''
    option_count = Array('d', [0 for _ in range(22)])

    # 보보보, 방방방, 피피피
    collision_count = Array('d', [0 for _ in range(3)])

    # 아이템 타입 dict
    item_type: dict = {1: 'Weapon', 2: 'SubWeapon', 3: 'Emblem'}

    # 아이템 타입 dict
    cube_type: dict = {0: 'Additional Cube', 1: 'Red Cube', 2: 'Black Cube'}

    # 잠재능력 테이블 dict
    set_potential_table: dict = {(1, 1) : get_table.getWeapon(), (1, 2) : get_table.getSubweapon(), (1, 3) : get_table.getEmblem(),
                                 (2, 1) : get_table.getBlackweapon(), (2, 2) : get_table.getBlacksubweapon(), (2, 3) : get_table.getBlackemblem()}
    
    # 시뮬레이션 선택
    set_simulation: dict = {1: simulation}
    
    while True:
        try:
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

            # 0은 에디셔널 큐브, 에디는 기본적으로 table_type이 1
            cube_input: int = 0
            table_input: int = 1

            # potential_input이 1이면 윗잠이므로, 세부 값 결정
            if potential_input == 1:
                print("\nSet Cube type ( 1: red, 2: black )")
                cube_input = int(sys.stdin.readline().strip())

                print("\nSet Cube Table ( 1: old( ~ 2021.08.11 ), 2: new( 2021.08.12 ~ ) )")
                table_input = int(sys.stdin.readline().strip())

            # cube_type, table_type exception check
            if cube_input not in [0, 1, 2] and table_input not in [1, 2]:
                raise NotDefinedNumberError

            # 결정된 확률 테이블
            set_table : List[list] = set_potential_table[(cube_input, select)]
            
            for option_table in set_table[:3]:
                select_option.append(option_table)

            for option_prob in set_table[-3:]:
                select_option_prob.append(option_prob)

            print("\nType sample size( >= 1 )")
            count: int = int(sys.stdin.readline().strip())
            
            # 확률 체크 용 print 디버깅
            # print(select_option_prob)
            # print(select_option)
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
                        p = Process(target = set_simulation[potential_input], args=(sample_list, option_count, collision_count, select_option, select_option_prob, iter_start, iter_end, print_log))
                        p.start()
                        processes.append(p)
                        iter_start = iter_end
                        iter_end = round((i + 2) * count / num_process)
                    
                    for p in processes:
                        p.join()
                        p.close()
                    
                    nowtime: str = get_time()
                    resultmsg: str = ''

                    if select != 3:
                        resultmsg = concat_all(f"Result\n--------------------------------------------------------------------\n",
                                               f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n",
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
                                               f"Item Type : {item_type[select]}\nSample size : {count}\nCube Type : {cube_type[cube_input]}\n",
                                               f"--------------------------------------------------------------------\n",
                                               f"옵션 종류\n",
                                               f"공공공 : {int(option_count[0])}, {round(option_count[0] * 100 / count, 3)}%   ",
                                               f"공공방 : {int(option_count[2])}, {round(option_count[2] * 100 / count, 3)}%\n",
                                               f"공방방 : {int(option_count[5])}, {round(option_count[5] * 100 / count, 3)}%\n",
                                               f"마마마 : {int(option_count[6])}, {round(option_count[6] * 100 / count, 3)}%   ",
                                               f"마마방 : {int(option_count[8])}, {round(option_count[8] * 100 / count, 3)}%\n",
                                               f"마방방 : {int(option_count[11])}, {round(option_count[11] * 100 / count, 3)}%\n",
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