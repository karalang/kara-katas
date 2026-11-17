// LeetCode #2247: Maximum Cost of Trip With K Highways -- the benchmark's
// Go mirror of trip.kara: dynamic programming over subsets, masks in
// increasing order.
package main

import (
	"fmt"
	"math/bits"
)

type road struct{ to, toll int64 }

func maximumCost(n int, highways [][3]int64, k int) int64 {
	if k+1 > n {
		return -1
	}
	roads := make([][]road, n)
	for _, h := range highways {
		roads[h[0]] = append(roads[h[0]], road{h[1], h[2]})
		roads[h[1]] = append(roads[h[1]], road{h[0], h[2]})
	}
	full := 1 << n
	best := make([][]int64, full)
	for mask := range best {
		best[mask] = make([]int64, n)
		for v := range best[mask] {
			best[mask][v] = -1
		}
	}
	for v := 0; v < n; v++ {
		best[1<<v][v] = 0
	}
	answer := int64(-1)
	for mask := 1; mask < full; mask++ {
		cities := bits.OnesCount(uint(mask))
		for v := 0; v < n; v++ {
			cost := best[mask][v]
			if cost < 0 {
				continue
			}
			if cities == k+1 {
				answer = max(answer, cost)
				continue
			}
			for _, r := range roads[v] {
				if mask&(1<<r.to) == 0 {
					next := mask | (1 << r.to)
					best[next][r.to] = max(best[next][r.to], cost+r.toll)
				}
			}
		}
	}
	return answer
}

var seed int64 = 2247

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	check := int64(0)
	for t := 0; t < 16; t++ {
		pairs := [][2]int64{}
		for a := int64(0); a < 15; a++ {
			for b := a + 1; b < 15; b++ {
				pairs = append(pairs, [2]int64{a, b})
			}
		}
		for i := len(pairs) - 1; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			pairs[i], pairs[j] = pairs[j], pairs[i]
		}
		highways := make([][3]int64, 50)
		for i := 0; i < 50; i++ {
			highways[i] = [3]int64{pairs[i][0], pairs[i][1], nextRandom() % 101}
		}
		check = (check*31 + maximumCost(15, highways, 14) + 1) % 1000000007
	}
	fmt.Printf("16 maps of 15 cities: checksum %d\n", check)
}
