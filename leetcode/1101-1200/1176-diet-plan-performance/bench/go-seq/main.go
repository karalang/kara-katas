// LeetCode #1176: Diet Plan Performance -- the ★ arm's bench in Go: one
// window of k days slid across the plan, its sum kept as it goes, each
// window scored as it is reached. The same plan and the same 2000 calls.
package main

import "fmt"

func dietPlanPerformance(calories []int64, k int64, lower int64, upper int64) int64 {
	var points, total int64
	for i, c := range calories {
		i := int64(i)
		total += c
		if i >= k {
			total -= calories[i-k]
		}
		if i >= k-1 {
			if total < lower {
				points--
			} else if total > upper {
				points++
			}
		}
	}
	return points
}

var seed int64 = 1176

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calories := make([]int64, 100000)
	for i := range calories {
		calories[i] = nextRandom() % 20001
	}
	calls := 2000
	var check int64
	for c := 0; c < calls; c++ {
		k := 1 + nextRandom()%100000
		mean := 10000 * k
		spread := nextRandom() % 100 * k
		p := dietPlanPerformance(calories, k, mean-spread, mean+spread)
		check = (check*131 + p + 100000) % 1000000007
	}
	fmt.Printf("%d calls: checksum %d\n", calls, check)
}
