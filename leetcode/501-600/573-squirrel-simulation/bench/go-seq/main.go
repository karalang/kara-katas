// Benchmark for #573: Go mirror of the ★ arm (one pass with the best
// first nut); see min_distance.kara.
package main

import (
	"fmt"
	"math"
)

func abs64(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func distance(a, b []int64) int64 {
	return abs64(a[0]-b[0]) + abs64(a[1]-b[1])
}

func minDistance(height, width int64, tree, squirrel []int64, nuts [][]int64) int64 {
	var total int64 = 0
	var bestSaving int64 = math.MinInt64
	for _, nut := range nuts {
		toTree := distance(nut, tree)
		total += 2 * toTree
		bestSaving = max(bestSaving, toTree-distance(nut, squirrel))
	}
	return total - bestSaving
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func cell(seed *int64) []int64 {
	r := nextRandom(seed) % 100
	return []int64{r, nextRandom(seed) % 100}
}

func main() {
	var count int64 = 20
	var rounds int64 = 2000
	var seed int64 = 573
	trees := make([][]int64, 0, count)
	squirrels := make([][]int64, 0, count)
	nutSets := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		trees = append(trees, cell(&seed))
		squirrels = append(squirrels, cell(&seed))
		nuts := make([][]int64, 0, 5000)
		for i := 0; i < 5000; i++ {
			nuts = append(nuts, cell(&seed))
		}
		nutSets = append(nutSets, nuts)
	}
	var total int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := minDistance(100, 100, trees[p], squirrels[p], nutSets[p])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d cases of 5000 nuts, %d rounds: %d steps, checksum %d\n", count, rounds, total, checksum)
}
