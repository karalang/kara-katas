// Benchmark for #447: mirror of number_of_boomerangs.kara (a map of
// distances per point) on 10 random sets of 1,000 distinct points on a
// 300 x 300 grid, built once.
package main

import "fmt"

type point struct{ x, y int64 }

func numberOfBoomerangs(points []point) int64 {
	total := int64(0)
	for _, p := range points {
		counts := map[int64]int64{}
		for _, q := range points {
			dx := p.x - q.x
			dy := p.y - q.y
			counts[dx*dx+dy*dy]++
		}
		for _, c := range counts {
			total += c * (c - 1)
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n = 10, 1000
	seed := int64(447)
	sets := make([][]point, 0, count)
	for c := 0; c < count; c++ {
		seen := map[point]bool{}
		points := make([]point, 0, n)
		for len(points) < n {
			x := nextRandom(&seed) % 300
			y := nextRandom(&seed) % 300
			if !seen[point{x, y}] {
				seen[point{x, y}] = true
				points = append(points, point{x, y})
			}
		}
		sets = append(sets, points)
	}
	total := int64(0)
	checksum := int64(0)
	for _, points := range sets {
		answer := numberOfBoomerangs(points)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d sets of %d points: %d boomerangs, checksum %d\n", count, n, total, checksum)
}
