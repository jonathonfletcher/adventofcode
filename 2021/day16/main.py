from functools import reduce
import os
import inspect

class P1(object):

    def __init__(self) -> None:
        self.version_sum = 0
        self.operators = {
            '000': self.operand_sum,
            '001': self.operand_prod,
            '010': self.operand_min,
            '011': self.operand_max,
            '101': self.operand_gt,
            '110': self.operand_lt,
            '111': self.operand_eq
        }

    def operand_sum(self, stack):
        r = reduce(lambda x, y: x+y, stack)
        # print(f'sum({stack}) -> {r}')
        return r

    def operand_prod(self, stack):
        r = reduce(lambda x, y: x*y, stack)
        # print(f'prod({stack}) -> {r}')
        return r

    def operand_min(self, stack):
        r = reduce(lambda x, y: min(x, y), stack)
        # print(f'min({stack}) -> {r}')
        return r

    def operand_max(self, stack):
        r = reduce(lambda x, y: max(x, y), stack)
        # print(f'max({stack}) -> {r}')
        return r

    def operand_gt(self, stack):
        r = 0
        if stack[0] > stack[1]:
            r = 1
        # print(f'gt({stack}) -> {r}')
        return r

    def operand_lt(self, stack):
        r = 0
        if stack[0] < stack[1]:
            r = 1
        # print(f'lt({stack}) -> {r}')
        return r

    def operand_eq(self, stack):
        r = 0
        if stack[0] == stack[1]:
            r = 1
        # print(f'eq({stack}) -> {r}')
        return r

    def process_XXX(self, packet:str, stack:list) -> str:
        # print(f'{len(packet)} {packet} {inspect.currentframe().f_code.co_name}')
        pkt_op_length, packet = packet[:1], packet[1:]
        if int(pkt_op_length, 2) == 0:
            sub_pkt_length, packet = packet[:15], packet[15:]
            # print(f'{pkt_op_length} {sub_pkt_length}')
            sub_length = int(sub_pkt_length, 2)
            sub_pkt, packet = packet[:sub_length], packet[sub_length:]
            while len(sub_pkt):
                sub_pkt = self.process(sub_pkt, stack)
            return packet
        else:
            sub_pkt_count, packet = packet[:11], packet[11:]
            # print(f'{pkt_op_length} {sub_pkt_count}')
            for i in range(int(sub_pkt_count, 2)):
                packet = self.process(packet, stack)
            return packet


    def process_100(self, packet:str, stack:list) -> str:
        # print(f'{len(packet)} {packet} {inspect.currentframe().f_code.co_name}')
        group_val = ""
        while True:
            pkt_group, pkt_group_val, packet = packet[0], packet[1:5], packet[5:]
            group_val += pkt_group_val
            if int(pkt_group, 2) != 1:
                break
        stack.append(int(group_val, 2))
        return packet


    def process(self, packet:str, stack:list) -> str:
        if not ( len(packet) and packet.count('1') > 0 ):
            return ''

        pkt_version, pkt_type, packet = packet[:3], packet[3:6], packet[6:]
        # print(f'{pkt_version} {pkt_type} {packet}')
        self.version_sum += int(pkt_version, 2)
        if pkt_type == '100':
            packet = self.process_100(packet, stack)
        else:
            sub_stack = []
            packet = self.process_XXX(packet, sub_stack)
            operator = self.operators.get(pkt_type)
            if operator is not None:
                op_result = operator(sub_stack)
                stack.append(op_result)
        return packet





part_one_tests = [
    ["8A004A801A8002F478", 16],
    ["620080001611562C8802118E34", 12],
    ["C0015000016115A2E0802F182340", 23],
    ["A0016C880162017C3686B18A3D4780", 31]
]

part_two_tests = [
    ["C200B40A82", 3],
    ["04005AC33890", 54],
    ["CE00C43D881120", 9],
    ["D8005AC2A8F0", 1],
    ["F600BC2D8F", 0],
    ["9C005AC2F8F0", 0],
    ["9C0141080250320F1802104A08", 1]
]

if False:
    pass_tests = True
    for input, output in part_two_tests:
        packet = ''.join([format(i, f'04b') for i in
            [int(x, 16) for x in input]])
        print(f'{input} - {packet}')
        p = P1()
        s = []
        p.process(packet, s)
        # print(p.result)
        # print(p.results)
        # print(s)
        # r = Runner()
        # result = r.run(s[0])
        if len(s) != 1:
            pass_tests = False
        if s[0] != output:
            pass_tests = False
        if not pass_tests:
            break
    if pass_tests:
        print("PASS")
    else:
        print("FAIL")

if True:
    with open('part1.txt') as ifp:
        input = ifp.readline().strip()
        packet = ''.join([format(i, f'04b') for i in
            [int(x, 16) for x in input]])
        # print(f'{input} - {packet}')
        p = P1()
        s = []
        p.process(packet, s)
        print(p.version_sum)
        print(s[0])


