// LeetCode #2861: Maximum Number of Alloys -- the bench: the ★ arm over
// 100 cases of 100 metals and 100 machines, LeetCode's most, amounts
// drawn over LeetCode's full ranges, all drawn first, then each
// answered 20 times.
package main

import "fmt"

func maxNumberOfAlloys(n int, budget int64, composition [][]int64, stock, cost []int64) int64 {
	var best int64
	for _, machine := range composition {
		price := func(x int64) int64 {
			var sum int64
			for j := 0; j < n; j++ {
				sum += max(machine[j]*x-stock[j], 0) * cost[j]
			}
			return sum
		}
		var lo, hi int64 = 0, 200000000
		for lo < hi {
			mid := (lo + hi + 1) / 2
			if price(mid) <= budget {
				lo = mid
			} else {
				hi = mid - 1
			}
		}
		best = max(best, lo)
	}
	return best
}

var seed int64 = 2861

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

type kase struct {
	budget      int64
	composition [][]int64
	stock, cost []int64
}

func main() {
	const count, rounds, n = 100, 20, 100
	cases := make([]kase, count)
	for c := range cases {
		comp := make([][]int64, n)
		for i := range comp {
			comp[i] = make([]int64, n)
			for j := range comp[i] {
				comp[i][j] = 1 + wide()%100
			}
		}
		stock := make([]int64, n)
		for j := range stock {
			stock[j] = wide() % 100000001
		}
		cost := make([]int64, n)
		for j := range cost {
			cost[j] = 1 + wide()%100
		}
		cases[c] = kase{wide() % 100000001, comp, stock, cost}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, t := range cases {
			alloys := maxNumberOfAlloys(n, t.budget, t.composition, t.stock, t.cost)
			total += alloys
			check = (check*31 + alloys + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d by %d, %d rounds: %d alloys, checksum %d\n", count, n, n, rounds, total, check)
}
