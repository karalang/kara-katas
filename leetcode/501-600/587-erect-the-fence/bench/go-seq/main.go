// Benchmark for #587: Go mirror of the ★ arm (the monotone chain); see
// ../outer_trees.kara. Each call copies the trees into a fresh slice,
// sorts it with slices.SortFunc, and removes repeats with slices.Compact.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type point struct{ x, y int64 }

func compare(a, b point) int {
	if c := cmp.Compare(a.x, b.x); c != 0 {
		return c
	}
	return cmp.Compare(a.y, b.y)
}

func cross(o, a, b point) int64 {
	return (a.x-o.x)*(b.y-o.y) - (a.y-o.y)*(b.x-o.x)
}

func outerTrees(trees []point) []point {
	points := slices.Clone(trees)
	slices.SortFunc(points, compare)
	fence := []point{}
	for _, p := range points {
		for len(fence) >= 2 && cross(fence[len(fence)-2], fence[len(fence)-1], p) < 0 {
			fence = fence[:len(fence)-1]
		}
		fence = append(fence, p)
	}
	lower := len(fence)
	for i := len(points) - 1; i >= 0; i-- {
		p := points[i]
		for len(fence) > lower && cross(fence[len(fence)-2], fence[len(fence)-1], p) < 0 {
			fence = fence[:len(fence)-1]
		}
		fence = append(fence, p)
	}
	slices.SortFunc(fence, compare)
	return slices.Compact(fence)
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var count, rounds int64 = 50, 300
	var seed int64 = 587
	gardens := [][]point{}
	for g := int64(0); g < count; g++ {
		size := 1000 + nextRandom(&seed)%2001
		taken := make([]bool, 101*101)
		trees := []point{}
		for int64(len(trees)) < size {
			x := nextRandom(&seed) % 101
			y := nextRandom(&seed) % 101
			if !taken[x*101+y] {
				taken[x*101+y] = true
				trees = append(trees, point{x, y})
			}
		}
		gardens = append(gardens, trees)
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			fence := outerTrees(gardens[p])
			var sum int64
			for _, t := range fence {
				sum += t.x*101 + t.y
			}
			total += int64(len(fence))
			checksum = (checksum*31 + sum) % 1000000007
		}
	}
	fmt.Printf("%d gardens, %d rounds: %d on the fence, checksum %d\n", count, rounds, total, checksum)
}
