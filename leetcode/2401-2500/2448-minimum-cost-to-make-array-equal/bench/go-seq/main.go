// LeetCode #2448: Minimum Cost to Make Array Equal -- the bench, the ★
// arm: the pairs sorted, the weighted median the first value whose
// running cost reaches half the total, and every value moved there.
package main

import (
	"fmt"
	"sort"
)

type pair struct{ value, cost int64 }

func minCost(nums, cost []int64) int64 {
	pairs := make([]pair, len(nums))
	var total int64
	for i := range nums {
		pairs[i] = pair{nums[i], cost[i]}
		total += cost[i]
	}
	sort.Slice(pairs, func(a, b int) bool {
		if pairs[a].value != pairs[b].value {
			return pairs[a].value < pairs[b].value
		}
		return pairs[a].cost < pairs[b].cost
	})
	var running, target int64
	for _, p := range pairs {
		running += p.cost
		if 2*running >= total {
			target = p.value
			break
		}
	}
	var answer int64
	for i := range nums {
		d := nums[i] - target
		if d < 0 {
			d = -d
		}
		answer += d * cost[i]
	}
	return answer
}

var seed int64 = 2448

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	nums := make([]int64, n)
	cost := make([]int64, n)
	for i := 0; i < n; i++ {
		r := nextRandom()
		nums[i] = 1 + (r*32768+nextRandom())%1000000
		r = nextRandom()
		cost[i] = 1 + (r*32768+nextRandom())%1000000
	}
	var check int64
	for p := int64(0); p < 200; p++ {
		for t := int64(0); t < 1000; t++ {
			cost[(1000*p+t)%n] = 1 + nextRandom()*30
		}
		check = (check*31 + minCost(nums, cost)%1000000007 + p) % 1000000007
	}
	fmt.Printf("200 passes over 10^5 values: checksum %d\n", check)
}
