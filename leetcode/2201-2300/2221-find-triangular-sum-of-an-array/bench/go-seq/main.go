// LeetCode #2221: Find Triangular Sum of an Array -- bench mirror of
// triangle.kara: the rounds done in place, each writing
// (nums[i] + nums[i + 1]) % 10 over nums[i].
package main

import "fmt"

func triangularSum(nums []int64) int64 {
	row := append([]int64(nil), nums...)
	n := len(row)
	for live := n - 1; live >= 1; live-- {
		for i := 0; i < live; i++ {
			row[i] = (row[i] + row[i+1]) % 10
		}
	}
	return row[0]
}

var seed int64 = 2221

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var arrays [][]int64
	for a := 0; a < 8; a++ {
		// 1000 digits, the constraints' largest
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = nextRandom() % 10
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for a := 0; a < 8; a++ {
		for r := 0; r < 8; r++ {
			// punch: one digit is drawn again before each answer
			arrays[a][r*113] = nextRandom() % 10
			check = (check*31 + triangularSum(arrays[a])) % 1000000007
		}
	}
	fmt.Printf("8 arrays of 1000 digits, 8 punches: checksum %d\n", check)
}
