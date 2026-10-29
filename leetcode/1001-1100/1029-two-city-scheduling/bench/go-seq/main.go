// LeetCode #1029: Two City Scheduling -- bench
// Mirrors ../two_city.kara; see ../../README.md § Benchmarks.

package main

import (
	"fmt"
	"sort"
)

func twoCitySchedCost(costs [][]int64) int64 {
	order := make([][]int64, len(costs))
	copy(order, costs)
	sort.SliceStable(order, func(i, j int) bool {
		return order[i][0]-order[i][1] < order[j][0]-order[j][1]
	})
	half := len(order) / 2
	total := int64(0)
	for i := range order {
		if i < half {
			total += order[i][0]
		} else {
			total += order[i][1]
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 1000, 100
	seed := int64(1029)
	cases := [][][]int64{}
	for k := 0; k < count; k++ {
		costs := [][]int64{}
		for p := 0; p < 100; p++ {
			a := nextRandom(&seed)%1000 + 1
			b := nextRandom(&seed)%1000 + 1
			costs = append(costs, []int64{a, b})
		}
		cases = append(cases, costs)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, costs := range cases {
			answer := twoCitySchedCost(costs)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d cases of 100 people, %d rounds: sum %d, checksum %d\n", count, rounds, total, check)
}
