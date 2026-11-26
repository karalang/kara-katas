// LeetCode #1774: Closest Dessert Cost -- the bench in Go, mirroring
// closest_cost.kara: a depth-first search over the toppings for each base.
package main

import "fmt"

func abs32(x int32) int32 {
	if x < 0 {
		return -x
	}
	return x
}

func better(cost, best, target int32) bool {
	d, e := abs32(cost-target), abs32(best-target)
	return d < e || (d == e && cost < best)
}

func addToppings(toppings []int32, i int, cost, target int32, best *int32) {
	if better(cost, *best, target) {
		*best = cost
	}
	if i == len(toppings) || cost >= target {
		return
	}
	for times := int32(0); times < 3; times++ {
		addToppings(toppings, i+1, cost+times*toppings[i], target, best)
	}
}

func closestCost(baseCosts, toppingCosts []int32, target int32) int32 {
	best := baseCosts[0]
	for _, base := range baseCosts {
		addToppings(toppingCosts, 0, base, target, &best)
	}
	return best
}

var seed int64 = 1774

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomCosts(n int, most int64) []int32 {
	v := make([]int32, n)
	for i := range v {
		v[i] = int32(1 + nextRandom()%most)
	}
	return v
}

func main() {
	bases := make([][]int32, 100)
	toppings := make([][]int32, 100)
	for r := 0; r < 100; r++ {
		bases[r] = randomCosts(10, 5000)
		toppings[r] = randomCosts(8, 1000)
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		target := int32(1 + (check+call*7919)%10000)
		cost := closestCost(bases[(check+call)%100], toppings[(check/100+call*31)%100], target)
		check = (check*31 + int64(cost)) % 1000000007
	}
	fmt.Printf("1000 calls over 100 menus: checksum %d\n", check)
}
