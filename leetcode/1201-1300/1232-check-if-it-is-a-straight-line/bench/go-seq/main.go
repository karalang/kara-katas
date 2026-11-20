// LeetCode #1232 bench: the ★ arm in Go, over the same 1000 sets of 1000
// points and 200 passes as the Kāra bench.
package main

import "fmt"

func checkStraightLine(coordinates [][]int64) bool {
	dx := coordinates[1][0] - coordinates[0][0]
	dy := coordinates[1][1] - coordinates[0][1]
	for _, p := range coordinates {
		if (p[0]-coordinates[0][0])*dy != (p[1]-coordinates[0][1])*dx {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1232)
	sets := make([][][]int64, 1000)
	for s := 0; s < 1000; s++ {
		dx := nextRandom(&seed)%21 - 10
		dy := nextRandom(&seed)%21 - 10
		if dx == 0 && dy == 0 {
			dx = 1
		}
		pts := make([][]int64, 1000)
		for t := int64(0); t < 1000; t++ {
			pts[t] = []int64{t * dx, t * dy}
		}
		if s%2 == 1 {
			if dx == 0 {
				pts[999][0]++
			} else {
				pts[999][1]++
			}
		}
		sets[s] = pts
	}
	straight := 0
	for pass := 0; pass < 200; pass++ {
		for _, pts := range sets {
			if checkStraightLine(pts) {
				straight++
			}
		}
	}
	fmt.Printf("1000 sets of 1000 points, 200 passes: %d straight\n", straight)
}
