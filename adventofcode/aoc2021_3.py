from downloader import download
import statistics
import numpy as np

download(2021, 3)
with open('aoc2021_3input.txt') as inputfile:
    #report = [int(line) for line in inputfile.readlines()]
    report = np.array([list(number) for number in inputfile.read().splitlines()])
print(report)

gamma = int(''.join(statistics.mode(row) for row in report.swapaxes(1, 0)), 2)
print(gamma)
epsilon = gamma ^ int('1' * 12, 2)
print(epsilon)
power_consumption = gamma * epsilon
print(power_consumption)

def filter_report(report, bit_criteria_is_most_common=True):
    index = 0
    while report.shape[0] > 1:
        try:
            bit_criteria = statistics.mode(report[:,index])
        except statistics.StatisticsError:
            bit_criteria = '1'
        if not bit_criteria_is_most_common:
            bit_criteria = str(int(not int(bit_criteria)))
        print(index, report.shape, bit_criteria)
        report = report[report[:,index] == bit_criteria]
        #print(report)
        index += 1
    return int(''.join(report[0]), 2)

print(filter_report(report.copy()) * filter_report(report.copy(), False))
