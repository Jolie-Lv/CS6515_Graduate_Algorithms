import unittest

from dynamic_programming import longest_increasing_subsequence, longest_common_subsequence, knapsack_no_repeat, knapsack_repeat

class TestDP(unittest.TestCase):

    def test_lis1(self):
        self.assertTrue(longest_increasing_subsequence([0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]) == 6)
    
    def test_lis2(self):
        self.assertTrue(longest_increasing_subsequence([5,8,3,7,9,1]) == 3)

    def test_lcs(self):
        self.assertTrue(longest_common_subsequence('ABCDGH','AEDFHR') == 3)

    def test_knapsack_no_repeat(self):
        self.assertTrue(knapsack_no_repeat([10,20,30],[60,100,120],50) == 220)

    def test_knapsack_repeat(self):
        self.assertTrue(knapsack_repeat([1,3,4,5],[10,40,50,70],8) == 110)

if __name__ == '__main__':
    unittest.main()
