// LeetCode #1770: Maximum Score from Performing Multiplication Operations
// -- the bench in Go, mirroring maximum_score.kara: one row of the table,
// filled from the last operation back to the first.
package main

import "fmt"

func maximumScore(nums []int32, multipliers []int32) int32 {
	n := len(nums)
	m := len(multipliers)
	best := make([]int32, m+1)
	for i := m - 1; i >= 0; i-- {
		for left := 0; left <= i; left++ {
			right := n - 1 - (i - left)
			takeLeft := multipliers[i]*nums[left] + best[left+1]
			takeRight := multipliers[i]*nums[right] + best[left]
			best[left] = max(takeLeft, takeRight)
		}
	}
	return best[0]
}

var seed int64 = 1770

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomNumbers(n int) []int32 {
	v := make([]int32, n)
	for i := range v {
		v[i] = int32(nextRandom()%2001 - 1000)
	}
	return v
}

func main() {
	numbers := make([][]int32, 100)
	for r := range numbers {
		numbers[r] = randomNumbers(1000)
	}
	weights := make([][]int32, 100)
	for r := range weights {
		weights[r] = randomNumbers(300)
	}
	var check int64
	for call := int64(0); call < 2000; call++ {
		score := maximumScore(numbers[(check+call*7919)%100], weights[(check/100+call)%100])
		check = (check*31 + int64(score)%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("2000 calls over 100 lists: checksum %d\n", check)
}
