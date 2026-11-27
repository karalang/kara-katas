// LeetCode #1827: Minimum Operations to Make the Array Increasing -- the bench
// in Go: the ★ arm over 10000 calls on runs of 2500 to 4999 numbers cut from
// one list of 10^4 numbers from 1 to 10^4, built once, each run's start and
// length drawn from the checksum so far.
package main

import (
	"fmt"
	"slices"
)

func minOperations(nums []int64) int64 {
	var operations, last int64
	for _, x := range nums {
		if x <= last {
			last++
			operations += last - x
		} else {
			last = x
		}
	}
	return operations
}

var seed int64 = 1827

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 10000)
	for i := range base {
		base[i] = 1 + nextRandom()%10000
	}
	var check int64
	for call := int64(0); call < 10000; call++ {
		start := (check + call) % 5000
		length := 2500 + (check*7+call)%2500
		run := slices.Clone(base[start : start+length])
		check = (check*31 + minOperations(run)) % 1000000007
	}
	fmt.Printf("10000 calls: checksum %d\n", check)
}
