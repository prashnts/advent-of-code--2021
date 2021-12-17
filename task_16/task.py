import os

from collections import namedtuple


__here__ = os.path.dirname(__file__)

TEST_DATA_0 = 'D2FE28'
TEST_DATA_1 = '8A004A801A8002F478'
TEST_DATA_2 = '620080001611562C8802118E34'
TEST_DATA_3 = 'C0015000016115A2E0802F182340'
TEST_DATA_4 = 'A0016C880162017C3686B18A3D4780'


Packet = namedtuple('Packet', ['version', 'type_id', 'data'])


class BitsParser:
    def __init__(self, encoded: str):
        self.bits = self._parse_encoded(encoded)
        self.pos = 0

    def _parse_encoded(self, encoded: str) -> str:
        hex_to_bits = lambda x: bin(int(x, base=16))[2:].zfill(4)
        return ''.join(map(hex_to_bits, encoded))

    def yield_bits(self, nbits: int):
        bslice = self.bits[self.pos:self.pos + nbits]
        self.pos += nbits
        return bslice

    def yield_digit(self, nbits: int):
        return int(self.yield_bits(nbits), base=2)

    def parse_literal_data(self) -> int:
        nums = []
        while True:
            group = self.yield_bits(5)
            nums.append(group[1:])
            if group[0] == '0':
                # stop reading! Otherwise continue
                break
        return int(''.join(nums), base=2)

    def parse_n_packets(self, nb: int):
        return [self.parse_packet() for _ in range(nb)]

    def parse_len_packets(self, total_len: int):
        goal = self.pos + total_len
        packets = []

        while self.pos < goal:
            packets.append(self.parse_packet())

        return packets

    def parse_operator_data(self):
        length_type_id = self.yield_digit(1)
        if length_type_id == 1:
            nb_packets = self.yield_digit(11)
            return self.parse_n_packets(nb_packets)
        len_packets = self.yield_digit(15)
        return self.parse_len_packets(len_packets)

    def parse_packet_data(self, type_id):
        if type_id == 4:
            return self.parse_literal_data()
        return self.parse_operator_data()

    def parse_packet(self) -> Packet:
        version = self.yield_digit(3)
        type_id = self.yield_digit(3)
        data = self.parse_packet_data(type_id)
        return Packet(version, type_id, data)


def evaluate_packet(packet):
    if packet.type_id == 4:
        # literal packet.
        return packet.data
    if packet.type_id == 0:
        # sum packet.
        val = 0
        for pkt in packet.data:
            val += evaluate_packet(pkt)
        return val
    if packet.type_id == 1:
        # multiply packet.
        val = 1
        for pkt in packet.data:
            val *= evaluate_packet(pkt)
        return val
    if packet.type_id == 2:
        # minimum packet
        return min([evaluate_packet(pkt) for pkt in packet.data])
    if packet.type_id == 3:
        # maximum packet
        return max([evaluate_packet(pkt) for pkt in packet.data])
    if packet.type_id == 5:
        # greater than packet. Contains two packets.
        lhs, rhs = [evaluate_packet(pkt) for pkt in packet.data]
        return int(lhs > rhs)
    if packet.type_id == 6:
        # less than packet. Contains two packets.
        lhs, rhs = [evaluate_packet(pkt) for pkt in packet.data]
        return int(lhs < rhs)
    if packet.type_id == 7:
        # equal to packet. Contains two packets.
        lhs, rhs = [evaluate_packet(pkt) for pkt in packet.data]
        return int(lhs == rhs)


def calculate_1(data):
    bp = BitsParser(data)
    packet = bp.parse_packet()

    # We just need to sum all the packets versions now.
    def sum_versions(pkt):
        if type(pkt.data) == list:
            return pkt.version + sum([sum_versions(p) for p in pkt.data])
        return pkt.version

    return sum_versions(packet)


def calculate_2(data):
    bp = BitsParser(data)
    packet = bp.parse_packet()

    return evaluate_packet(packet)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA_0) == 6
    assert calculate_1(TEST_DATA_1) == 16
    assert calculate_1(TEST_DATA_2) == 12
    assert calculate_1(TEST_DATA_3) == 23
    assert calculate_1(TEST_DATA_4) == 31

    assert calculate_2('C200B40A82') == 3
    assert calculate_2('04005AC33890') == 54
    assert calculate_2('880086C3E88112') == 7
    assert calculate_2('CE00C43D881120') == 9
    assert calculate_2('D8005AC2A8F0') == 1
    assert calculate_2('F600BC2D8F') == 0
    assert calculate_2('9C005AC2F8F0') == 0
    assert calculate_2('9C0141080250320F1802104A08') == 1

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
