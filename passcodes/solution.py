import unittest
from collections import defaultdict

def naive(l):
    count = 0
    for i in range(0, len(l)-2):
        for j in range(i + 1, len(l)-1):
            for k in range(j +1, len(l)):
                if l[k] % l[j] == l[j] % l[i] == 0:
                    count += 1
                    print l[i], l[j], l[k]
    return count

def codes(l):
    x = defaultdict(int)
    y = defaultdict(int)
    count = 0
    for i in range(0, len(l)):
        num = l[i]
        for div in y.keys():
            if num % div == 0:
                count += y[div]
        for div in x.keys():
            if num % div == 0:
                y[num] += x[div]
        x[num] += 1
    return count

class TestCodes(unittest.TestCase):
    def test_solution(self):
        lists = [
            [1, 1, 1],
            [1, 3, 6],
            [1, 2, 3, 4, 5, 6, 12, 18, 24],
            [2]*10
        ]
        for l in lists:
            self.assertEqual(naive(l), codes(l))
