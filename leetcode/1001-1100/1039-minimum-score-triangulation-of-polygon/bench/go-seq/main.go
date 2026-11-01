// LeetCode #1039: Minimum Score Triangulation of Polygon -- bench
// Mirrors ../../triangulation.kara; see ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"math"
)

func minScoreTriangulation(values []int64) int64 {
	n := len(values)
	best := make([][]int64, n)
	for i := range best {
		best[i] = make([]int64, n)
	}
	for length := 2; length < n; length++ {
		for i := 0; i < n-length; i++ {
			j := i + length
			least := int64(math.MaxInt64)
			for k := i + 1; k < j; k++ {
				score := best[i][k] + best[k][j] + values[i]*values[k]*values[j]
				if score < least {
					least = score
				}
			}
			best[i][j] = least
		}
	}
	return best[0][n-1]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 2000, 10
	seed := int64(1039)
	polygons := make([][]int64, 0, count)
	for p := 0; p < count; p++ {
		values := make([]int64, 0, 50)
		for i := 0; i < 50; i++ {
			values = append(values, nextRandom(&seed)%100+1)
		}
		polygons = append(polygons, values)
	}
	total := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, values := range polygons {
			score := minScoreTriangulation(values)
			total += score
			check = (check*131 + score) % 1000000007
		}
	}
	fmt.Printf("%d polygons of 50 vertices, %d rounds: total %d, checksum %d\n", count, rounds, total, check)
}
