// LeetCode 787 — Cheapest Flights Within K Stops: the bench, in Go.
// Mirrors find_cheapest_price.kara: Bellman-Ford for k + 1 rounds, each
// round reading a fresh copy of the costs, over the same 64 networks.
package main

import (
	"fmt"
	"math"
)

func findCheapestPrice(n int64, flights [][3]int64, src, dst, k int64) int64 {
	const unreached = math.MaxInt64
	cost := make([]int64, n)
	for i := range cost {
		cost[i] = unreached
	}
	cost[src] = 0
	for round := int64(0); round < k+1; round++ {
		before := append([]int64(nil), cost...)
		for _, f := range flights {
			from, to, price := f[0], f[1], f[2]
			if before[from] != unreached && before[from]+price < cost[to] {
				cost[to] = before[from] + price
			}
		}
	}
	if cost[dst] == unreached {
		return -1
	}
	return cost[dst]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(787)
	networks := make([][][3]int64, 0, 64)
	for net := 0; net < 64; net++ {
		taken := make([]bool, 10000)
		flights := make([][3]int64, 0, 1000)
		for len(flights) < 1000 {
			from := nextRandom(&seed) % 100
			to := nextRandom(&seed) % 100
			if from != to && !taken[from*100+to] {
				taken[from*100+to] = true
				flights = append(flights, [3]int64{from, to, 1 + nextRandom(&seed)%10000})
			}
		}
		networks = append(networks, flights)
	}
	rounds := int64(20000)
	found, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		src := nextRandom(&seed) % 100
		dst := (src + 1 + nextRandom(&seed)%99) % 100
		k := nextRandom(&seed) % 100
		answer := findCheapestPrice(100, networks[r%64], src, dst, k)
		if answer != -1 {
			found++
		}
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("%d rounds of 100-city networks: %d with a way, checksum %d\n", rounds, found, check)
}
