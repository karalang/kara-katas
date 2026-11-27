// LeetCode #1829: Maximum XOR for Each Query -- the bench in Go: the ★ arm
// over 200 calls on the first 50000 to 99999 of one sorted list of 10^5
// numbers below 2^20, built once, each run's length drawn from the checksum so
// far, and maximumBit 20. Each call copies its run, as the arm takes its list
// by value.
package main

import (
	"fmt"
	"slices"
)

func getMaximumXor(nums []int64, maximumBit int64) []int64 {
	mask := int64(1)<<maximumBit - 1
	var all int64
	for _, x := range nums {
		all ^= x
	}
	answer := []int64{}
	for i := len(nums) - 1; i >= 0; i-- {
		answer = append(answer, all^mask)
		all ^= nums[i]
	}
	return answer
}

var seed int64 = 1829

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom()
		base = append(base, (hi*32768+nextRandom())%1048576)
	}
	slices.Sort(base)
	var check int64
	for call := int64(0); call < 200; call++ {
		n := 50000 + (check+call)%50000
		answer := getMaximumXor(slices.Clone(base[:n]), 20)
		var total int64
		for _, k := range answer {
			total += k
		}
		check = (check*31 + total%1000000007) % 1000000007
	}
	fmt.Printf("200 calls: checksum %d\n", check)
}
