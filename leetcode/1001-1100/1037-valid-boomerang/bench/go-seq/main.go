// LeetCode #1037: Valid Boomerang -- bench
// Mirrors ../../boomerang.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type point struct{ x, y int64 }

func isBoomerang(p []point) bool {
	return (p[1].x-p[0].x)*(p[2].y-p[0].y)-(p[1].y-p[0].y)*(p[2].x-p[0].x) != 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 1000000, 100
	seed := int64(1037)
	triples := make([][]point, 0)
	for i := 0; i < count; i++ {
		if i%3 == 0 {
			x := nextRandom(&seed) % 34
			y := nextRandom(&seed) % 34
			dx := nextRandom(&seed) % 34
			dy := nextRandom(&seed) % 34
			triples = append(triples, []point{{x, y}, {x + dx, y + dy}, {x + 2*dx, y + 2*dy}})
		} else {
			points := make([]point, 0)
			for k := 0; k < 3; k++ {
				x := nextRandom(&seed) % 101
				y := nextRandom(&seed) % 101
				points = append(points, point{x, y})
			}
			triples = append(triples, points)
		}
	}
	boomerangs := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, points := range triples {
			answer := isBoomerang(points)
			if answer {
				boomerangs++
			}
			add := int64(1)
			if answer {
				add = 2
			}
			check = (check*131 + add) % 1000000007
		}
	}
	fmt.Printf("%d triples, %d rounds: %d boomerangs, checksum %d\n", count, rounds, boomerangs, check)
}
