// LeetCode 812 -- Largest Triangle Area: the bench, with the ★ arm's
// every triple of points.
package main

import "fmt"

var seed int64 = 812

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type point struct{ x, y int64 }

func twiceArea(a, b, c point) int64 {
	v := (b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x)
	if v < 0 {
		return -v
	}
	return v
}

func largestTriangleArea(points []point) float64 {
	n := len(points)
	var best int64
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			for k := j + 1; k < n; k++ {
				twice := twiceArea(points[i], points[j], points[k])
				if twice > best {
					best = twice
				}
			}
		}
	}
	return float64(best) / 2.0
}

// A point with coordinates from -50 to 50 that is not in `points`.
func newPoint(points []point) point {
	for {
		p := point{nextRandom()%101 - 50, nextRandom()%101 - 50}
		taken := false
		for _, q := range points {
			if q == p {
				taken = true
			}
		}
		if !taken {
			return p
		}
	}
}

// 64 sets of 50 distinct points are made once. Each round moves one point
// of the next set to a new place and finds that set's largest triangle.
func main() {
	sets := make([][]point, 64)
	for k := range sets {
		for i := 0; i < 50; i++ {
			sets[k] = append(sets[k], newPoint(sets[k]))
		}
	}
	var rounds int64 = 60000
	total := 0.0
	var check int64
	for r := int64(0); r < rounds; r++ {
		k := r % 64
		p := newPoint(sets[k])
		sets[k][r/64%50] = p
		area := largestTriangleArea(sets[k])
		total += area
		check = (check*131 + int64(area*2.0)) % 1000000007
	}
	fmt.Printf("%d rounds of 50 points: total area %.1f, checksum %d\n", rounds, total, check)
}
