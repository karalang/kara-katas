// LeetCode #2216: Minimum Deletions to Make Array Beautiful -- bench
// mirror of beautiful.kara: a number that would start a pair is deleted
// when the number after it is the same; an odd length left costs one more.
package main

import "fmt"

func minDeletion(nums []int64) int64 {
	n := int64(len(nums))
	var deleted int64
	for i := int64(0); i < n-1; i++ {
		if (i-deleted)%2 == 0 && nums[i] == nums[i+1] {
			deleted++
		}
	}
	if (n-deleted)%2 == 1 {
		deleted++
	}
	return deleted
}

var seed int64 = 2216

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var arrays [][]int64
	for a := 0; a < 60; a++ {
		// 10^5 numbers up to 1, 3 and 10^5 in turn
		top := []int64{1, 3, 100000}[a%3]
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom() % (top + 1)
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for a := 0; a < 60; a++ {
		for r := 0; r < 20; r++ {
			// punch: one number takes its neighbour's value before each answer
			arrays[a][r*4999+1] = arrays[a][r*4999]
			check = (check*31 + minDeletion(arrays[a])) % 1000000007
		}
	}
	fmt.Printf("60 arrays of 10^5, 20 punches: checksum %d\n", check)
}
