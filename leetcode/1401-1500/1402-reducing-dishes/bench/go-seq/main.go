// LeetCode #1402 bench, Go: the same sort and running sum, workload and
// checksum as max_satisfaction.kara.
package main

import (
	"fmt"
	"sort"
)

func maxSatisfaction(satisfaction []int32) int32 {
	order := append([]int32(nil), satisfaction...)
	sort.Slice(order, func(i, j int) bool { return order[i] > order[j] })
	var running, total int32
	for _, s := range order {
		if running+s <= 0 {
			break
		}
		running += s
		total += running
	}
	return total
}

func main() {
	var seed int64 = 1402
	pool := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool = append(pool, int32(seed%2001-1000))
	}
	var check int64
	for r := int64(0); r < 20000; r++ {
		at := (check + r*7919) % 99501
		window := append([]int32(nil), pool[at:at+500]...)
		check = (check*131 + int64(maxSatisfaction(window))) % 1000000007
	}
	fmt.Printf("20000 windows of 500 dishes: checksum %d\n", check)
}
