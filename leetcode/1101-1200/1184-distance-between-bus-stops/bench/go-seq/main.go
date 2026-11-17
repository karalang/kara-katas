// LeetCode #1184: Distance Between Bus Stops -- the ★ arm in Go: the arc
// from the lower stop to the higher, against the whole ring less it.
package main

import "fmt"

func distanceBetweenBusStops(distance []int64, start, destination int64) int64 {
	from, to := min(start, destination), max(start, destination)
	total, oneWay := int64(0), int64(0)
	for _, d := range distance {
		total += d
	}
	for _, d := range distance[from:to] {
		oneWay += d
	}
	return min(oneWay, total-oneWay)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1184)
	rings := [][]int64{}
	pairs := [][2]int64{}
	for r := 0; r < 50; r++ {
		ring := make([]int64, 10000)
		for i := range ring {
			ring[i] = nextRandom(&seed) % 10001
		}
		rings = append(rings, ring)
		for k := 0; k < 200; k++ {
			start := nextRandom(&seed) % 10000
			destination := nextRandom(&seed) % 10000
			pairs = append(pairs, [2]int64{start, destination})
		}
	}
	rounds := 10
	check := int64(0)
	for round := 0; round < rounds; round++ {
		for r, ring := range rings {
			for k := 0; k < 200; k++ {
				p := pairs[r*200+k]
				check = (check*131 + distanceBetweenBusStops(ring, p[0], p[1]) + int64(round)) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds of 10000 queries over 50 rings: checksum %d\n", rounds, check)
}
