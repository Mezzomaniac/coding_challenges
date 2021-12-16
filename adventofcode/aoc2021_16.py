from downloader import download
import operator
from functools import reduce

download(2021, 16)
with open('aoc2021_16input.txt') as inputfile:
    data = inputfile.read().strip()
print(len(data))

packet = ''.join(bin(int(data, 16))[2:].zfill(4 * len(data)))
print(len(packet))

def parse(packet, subpacket_count=None):
    versions_total = 0
    while packet:
        packet = packet.rstrip('0')
        #print(len(packet), subpacket_count, versions_total)
        version = int(packet[:3], 2)
        versions_total += version
        type_id = int(packet[3:6], 2)
        packet = packet[6:]
        if type_id == 4:
            literal = []
            while packet:
                #print(len(packet), subpacket_count, versions_total)
                group, packet = packet[:5], packet[5:]
                literal.append(group[1:])
                if group[0] == '0':
                    literal = int(''.join(literal), 2)
                    break 
        else:
            length_type_id, packet = packet[0], packet[1:]
            if length_type_id == '0':
                bit_length, packet = int(packet[:15], 2), packet[15:]
                sub_packets, packet = packet[:bit_length], packet[bit_length:]
                versions_total += parse(sub_packets)
            else:
                subpacket_number, packet = int(packet[:11], 2), packet[11:]
                versions_sum, packet = parse(packet, subpacket_number)
                versions_total += versions_sum
        if isinstance(subpacket_count, int):
            subpacket_count -= 1
            if not subpacket_count:
                return (versions_total, packet)
    return versions_total

print(parse(packet))


class Bits:
    versions_total = 0
    
    def __init__(self, packet):
        self.packet = packet
    
    def parse(self, subpacket_count=None):
        values = []
        #print('a', len(self.packet), subpacket_count, values)
        while self.packet:
            #print('b', len(self.packet), subpacket_count, values)
            version = int(self.packet[:3], 2)
            Bits.versions_total += version
            type_id = int(self.packet[3:6], 2)
            self.packet = self.packet[6:]
            if type_id == 4:
                #print('c', len(self.packet), subpacket_count, values)
                literal = []
                while self.packet:
                    #print('d', len(self.packet), subpacket_count, values)
                    group, self.packet = self.packet[:5], self.packet[5:]
                    literal.append(group[1:])
                    if group[0] == '0':
                        #print('e', len(self.packet), subpacket_count, values)
                        literal = int(''.join(literal), 2)
                        values.append(literal)
                        #print(literal)
                        break 
            else:
                #print('f', len(self.packet), subpacket_count, values)
                length_type_id, self.packet = self.packet[0], self.packet[1:]
                if length_type_id == '0':
                    #print('g', len(self.packet), subpacket_count, values)
                    bit_length, self.packet = int(self.packet[:15], 2), self.packet[15:]
                    subpackets, self.packet = self.packet[:bit_length], self.packet[bit_length:]
                    sub_values = Bits(subpackets).parse()
                else:
                    #print('h', len(self.packet), subpacket_count, values)
                    subpacket_number, self.packet = int(self.packet[:11], 2), self.packet[11:]
                    sub_values = self.parse(subpacket_number)
                #print(type_id, sub_values)
                if type_id == 0:
                    result = sum(sub_values)
                elif type_id == 1:
                    result = reduce(operator.mul, sub_values)
                elif type_id == 2:
                    result = min(sub_values)
                elif type_id == 3:
                    result = max(sub_values)
                elif type_id == 5:
                    result = int(reduce(operator.gt, sub_values))
                elif type_id == 6:
                    result = int(reduce(operator.lt, sub_values))
                elif type_id == 7:
                    result = int(reduce(operator.eq, sub_values))
                values.append(result)
                #print(result)
            if isinstance(subpacket_count, int):
                #print('i', len(self.packet), subpacket_count, values)
                subpacket_count -= 1
                if not subpacket_count:
                    #print('j', len(self.packet), subpacket_count, values)
                    break
            if set(self.packet) == {'0'}:
                break
        #print('k', len(self.packet), subpacket_count, values)
        return values

print(Bits(packet).parse())

#5390786451322
