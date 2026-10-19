// LeetCode 774 — Minimize Max Distance to Gas Station: benchmark, the ★
// arm in Go. Sixty-four random roads of 2,000 stations, LeetCode's limit,
// spread over up to 10^8, each with k from 1 to 10^6, built once; ROUNDS
// rounds each solve the next of them.
package main

import "fmt"

const ROUNDS = 2000

func minmaxGasDist(stations []int64, k int64) float64 {
	lo, hi := 0.0, 0.0
	for i := 1; i < len(stations); i++ {
		gap := float64(stations[i] - stations[i-1])
		if gap > hi {
			hi = gap
		}
	}
	hi += 1.0
	for it := 0; it < 100; it++ {
		mid := (lo + hi) / 2.0
		var needed int64
		for i := 1; i < len(stations); i++ {
			needed += int64(float64(stations[i]-stations[i-1]) / mid)
		}
		if needed <= k {
			hi = mid
		} else {
			lo = mid
		}
	}
	longest := 0.0
	for i := 1; i < len(stations); i++ {
		gap := float64(stations[i] - stations[i-1])
		piece := gap / float64(int64(gap/hi)+1)
		if piece > longest {
			longest = piece
		}
	}
	return longest
}

var seed int64 = 774

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	roads := make([][]int64, 0, 64)
	ks := make([]int64, 0, 64)
	for r := 0; r < 64; r++ {
		stations := []int64{nextRandom() % 100}
		for i := 1; i < 2000; i++ {
			a := nextRandom()
			b := nextRandom()
			stations = append(stations, stations[len(stations)-1]+1+(a*32768+b)%50000)
		}
		roads = append(roads, stations)
		a := nextRandom()
		b := nextRandom()
		ks = append(ks, 1+(a*32768+b)%1000000)
	}
	total := 0.0
	for round := 0; round < ROUNDS; round++ {
		total += minmaxGasDist(roads[round%64], ks[round%64])
	}
	fmt.Printf("%d roads of 2000 stations: answers sum to %.5f\n", ROUNDS, total)
}
