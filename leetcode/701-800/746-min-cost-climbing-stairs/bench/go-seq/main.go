// LeetCode 746 — Min Cost Climbing Stairs, bench: the ★ arm (two running
// totals) on a staircase of 1000 steps whose costs keep changing.
// Mirrors min_cost_climbing_stairs.kara.
package main

import "fmt"

func minCostClimbingStairs(cost []int64) int64 {
	var before, here int64
	for i := 2; i <= len(cost); i++ {
		next := here + cost[i-1]
		if before+cost[i-2] < here+cost[i-1] {
			next = before + cost[i-2]
		}
		before = here
		here = next
	}
	return here
}

var seed int64 = 746

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 300000
	var n int64 = 1000
	cost := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		cost = append(cost, nextRandom()%1000)
	}
	var total int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < 5; c++ {
			i := nextRandom() % n
			cost[i] = nextRandom() % 1000
		}
		total += minCostClimbingStairs(cost)
	}
	fmt.Printf("%d rounds on 1000 steps: least costs sum to %d\n", rounds, total)
}
