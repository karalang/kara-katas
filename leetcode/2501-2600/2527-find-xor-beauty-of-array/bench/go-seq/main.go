// LeetCode #2527: Find Xor-Beauty of Array -- Go mirror of the benchmark
// (xor.kara): the same lists, passes, order and checksum.
package main

import "fmt"

func xorBeauty(nums []int64) int64 {
	var beauty int64
	for _, x := range nums {
		beauty ^= x
	}
	return beauty
}

var seed int64 = 2527

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	lists := make([][]int64, 1000)
	for t := range lists {
		lists[t] = make([]int64, 100)
		for j := range lists[t] {
			lists[t][j] = wideRandom()%1000000000 + 1
		}
	}
	const passes = 3000
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 1000
		for i := int64(0); i < 1000; i++ {
			check = (check*31 + xorBeauty(lists[(start+i)%1000]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 1000 lists of 100 numbers: checksum %d\n", passes, check)
}
