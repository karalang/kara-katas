// Benchmark for #575: Go mirror of the ★ arm (a set of the types); see
// ../distribute_candies.kara. A fresh map with no size hint for every
// call, as the Kāra arm makes a fresh `Set[i64]`.
package main

import "fmt"

func distributeCandies(candyType []int64) int64 {
	kinds := map[int64]struct{}{}
	for _, c := range candyType {
		kinds[c] = struct{}{}
	}
	return min(int64(len(kinds)), int64(len(candyType))/2)
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var count int64 = 100
	var rounds int64 = 200
	var seed int64 = 575
	cases := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		types := 1 + nextRandom(&seed)%10000
		pool := make([]int64, 0, types)
		for i := int64(0); i < types; i++ {
			high := nextRandom(&seed) * 32768
			pool = append(pool, (high+nextRandom(&seed))%200001-100000)
		}
		candies := make([]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			candies = append(candies, pool[nextRandom(&seed)%types])
		}
		cases = append(cases, candies)
	}
	var total int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := distributeCandies(cases[p])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d cases of 10000 candies, %d rounds: %d types eaten, checksum %d\n", count, rounds, total, checksum)
}
