// Benchmark for #455: mirror of assign_cookies.kara (the ★ arm, both
// sorted, least greedy child first) on the same workload.
package main

import (
	"fmt"
	"slices"
)

func findContentChildren(g, s []int64) int64 {
	greed := slices.Clone(g)
	slices.Sort(greed)
	sizes := slices.Clone(s)
	slices.Sort(sizes)
	child := 0
	for _, size := range sizes {
		if child < len(greed) && size >= greed[child] {
			child++
		}
	}
	return int64(child)
}

// ---- benchmark --------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64) int64 {
	hi := nextRandom(seed)
	lo := nextRandom(seed)
	return 1 + (hi*65536+lo)%1000000000
}

func main() {
	const n = 1000000
	const rounds = 10
	var seed int64 = 455
	g := make([]int64, 0, n)
	s := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		g = append(g, randomValue(&seed))
		s = append(s, randomValue(&seed))
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		g[(hi*65536+lo)%n] = randomValue(&seed)
		hi = nextRandom(&seed)
		lo = nextRandom(&seed)
		s[(hi*65536+lo)%n] = randomValue(&seed)
		fed := findContentChildren(g, s)
		total += fed
		checksum = (checksum*31 + fed) % 1000000007
	}
	fmt.Printf("%d rounds on %d children and %d cookies: %d content, checksum %d\n", rounds, n, n, total, checksum)
}
