// Benchmark for #452: mirror of min_arrows.kara (greedy by end) on 10
// random sets of 100,000 balloons over the 32-bit range, built once,
// then each counted 10 times.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type balloon struct {
	start, end int64
}

func findMinArrowShots(points []balloon) int64 {
	byEnd := make([]balloon, len(points))
	copy(byEnd, points)
	slices.SortStableFunc(byEnd, func(a, b balloon) int { return cmp.Compare(a.end, b.end) })
	arrows, arrow := int64(0), int64(0)
	for _, b := range byEnd {
		if arrows == 0 || b.start > arrow {
			arrows++
			arrow = b.end
		}
	}
	return arrows
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const sets, n, rounds = 10, 100000, 10
	seed := int64(452)
	all := [][]balloon{}
	for s := 0; s < sets; s++ {
		points := make([]balloon, 0, n)
		for i := 0; i < n; i++ {
			r := nextRandom(&seed) * 65536
			r = (r + nextRandom(&seed)) * 2
			r += nextRandom(&seed) % 2
			start := r - 2147483648
			w := nextRandom(&seed) * 65536
			w = (w + nextRandom(&seed)) % 100000
			end := start + w
			if end > 2147483647 {
				end = 2147483647
			}
			points = append(points, balloon{start, end})
		}
		all = append(all, points)
	}
	total, checksum := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for _, points := range all {
			arrows := findMinArrowShots(points)
			total += arrows
			checksum = (checksum*31 + arrows) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d sets of %d: %d arrows, checksum %d\n", rounds, sets, n, total, checksum)
}
