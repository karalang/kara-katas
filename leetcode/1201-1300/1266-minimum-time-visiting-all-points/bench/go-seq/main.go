// LeetCode #1266 bench, in Go: the ★ arm (the larger of the two gaps
// between neighbouring points, summed over each pair of neighbours) on 1000
// random walks of 100 points from -1000 to 1000 built once, 3000 rounds;
// every answer folded into a checksum.
package main

import "fmt"

func gap(a, b int64) int64 {
	if a > b {
		return a - b
	}
	return b - a
}

func minTimeToVisitAllPoints(points [][]int64) int64 {
	var time int64
	for i := 1; i < len(points); i++ {
		time += max(gap(points[i][0], points[i-1][0]), gap(points[i][1], points[i-1][1]))
	}
	return time
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1266)
	walks := make([][][]int64, 1000)
	for w := range walks {
		walks[w] = make([][]int64, 100)
		for i := range walks[w] {
			x := nextRandom(&seed)%2001 - 1000
			y := nextRandom(&seed)%2001 - 1000
			walks[w][i] = []int64{x, y}
		}
	}
	var check int64
	for round := int64(0); round < 3000; round++ {
		for _, w := range walks {
			check = (check*131 + minTimeToVisitAllPoints(w) + round) % 1000000007
		}
	}
	fmt.Printf("3000 rounds of 1000 walks of 100 points: checksum %d\n", check)
}
