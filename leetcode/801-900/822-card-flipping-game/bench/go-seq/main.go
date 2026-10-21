// Benchmark for #822: Card Flipping Game -- the ★ arm (a set of the doubles).
//
// Mirrors flipgame.kara: the numbers on both sides of one card go in a
// set, and the answer is the smallest number on any card that is not in
// it, or 0.
package main

import "fmt"

func flipgame(fronts, backs []int64) int64 {
	doubles := make(map[int64]struct{})
	for i := range fronts {
		if fronts[i] == backs[i] {
			doubles[fronts[i]] = struct{}{}
		}
	}
	var best int64
	for i := range fronts {
		for _, x := range [2]int64{fronts[i], backs[i]} {
			if _, ok := doubles[x]; !ok && (best == 0 || x < best) {
				best = x
			}
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 64
	rounds := 50000
	seed := int64(822)
	allFronts := make([][]int64, 0, count)
	allBacks := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		fronts := make([]int64, 0, 1000)
		backs := make([]int64, 0, 1000)
		for i := 0; i < 1000; i++ {
			f := 1 + nextRandom(&seed)%2000
			fronts = append(fronts, f)
			if nextRandom(&seed)%2 == 0 {
				backs = append(backs, f)
			} else {
				backs = append(backs, 1+nextRandom(&seed)%2000)
			}
		}
		allFronts = append(allFronts, fronts)
		allBacks = append(allBacks, backs)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		answer := flipgame(allFronts[g], allBacks[g])
		total += answer
		checksum = (checksum*131 + answer) % 1000000007
	}
	fmt.Printf("%d rounds of %d hands: total %d, checksum %d\n", rounds, count, total, checksum)
}
