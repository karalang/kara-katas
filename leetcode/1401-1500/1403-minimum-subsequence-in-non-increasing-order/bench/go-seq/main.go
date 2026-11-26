// LeetCode #1403 bench, Go: the same sort and greedy take, workload and
// checksum as min_subsequence.kara.
package main

import (
	"fmt"
	"sort"
)

func minSubsequence(nums []int32) []int32 {
	order := append([]int32(nil), nums...)
	sort.Slice(order, func(i, j int) bool { return order[i] > order[j] })
	var rest int32
	for _, x := range order {
		rest += x
	}
	var taken int64
	picked := []int32{}
	for _, x := range order {
		picked = append(picked, x)
		taken += int64(x)
		rest -= x
		if taken > int64(rest) {
			break
		}
	}
	return picked
}

func main() {
	var seed int64 = 1403
	pool := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool = append(pool, int32(seed/65536%100+1))
	}
	var check int64
	for r := int64(0); r < 20000; r++ {
		at := (check + r*7919) % 99501
		window := append([]int32(nil), pool[at:at+500]...)
		picked := minSubsequence(window)
		last := int64(picked[len(picked)-1])
		check = (check*131 + int64(len(picked))*101 + last) % 1000000007
	}
	fmt.Printf("20000 windows of 500 numbers: checksum %d\n", check)
}
