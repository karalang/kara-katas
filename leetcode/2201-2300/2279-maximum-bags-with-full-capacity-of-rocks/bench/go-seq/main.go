// LeetCode #2279: Maximum Bags With Full Capacity of Rocks -- the bench,
// the ★ arm.
package main

import (
	"fmt"
	"sort"
)

func maximumBags(capacity, rocks []int64, additionalRocks int64) int64 {
	lack := make([]int64, 0)
	for i := range capacity {
		lack = append(lack, capacity[i]-rocks[i])
	}
	sort.Slice(lack, func(a, b int) bool { return lack[a] < lack[b] })
	left := additionalRocks
	var full int64
	for _, need := range lack {
		if need > left {
			break
		}
		left -= need
		full++
	}
	return full
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2279

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw(high int64) int64 {
	top := nextRandom()
	return (top*32768 + nextRandom()) % high
}

func main() {
	var check int64
	for t := 0; t < 50; t++ {
		capacity := make([]int64, 0)
		rocks := make([]int64, 0)
		for i := 0; i < 50000; i++ {
			c := draw(1000000000) + 1
			capacity = append(capacity, c)
			rocks = append(rocks, draw(c+1))
		}
		spare := draw(1000000000) + 1
		check = (check*31 + maximumBags(capacity, rocks, spare)) % 1000000007
	}
	fmt.Printf("50 sets of 5 * 10^4: checksum %d\n", check)
}
