// Benchmark for #469: mirror of convex_polygon.kara (the ★ arm: the sign
// of every turn) on the same workload.
package main

import "fmt"

type point struct {
	x, y int64
}

func isConvex(points []point) bool {
	n := len(points)
	sign := 0
	for i := 0; i < n; i++ {
		p0 := points[i]
		p1 := points[(i+1)%n]
		p2 := points[(i+2)%n]
		cross := (p1.x-p0.x)*(p2.y-p1.y) - (p1.y-p0.y)*(p2.x-p1.x)
		if cross != 0 {
			s := -1
			if cross > 0 {
				s = 1
			}
			if sign == 0 {
				sign = s
			} else if s != sign {
				return false
			}
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func polygon(n int64, dent bool, seed *int64) []point {
	points := make([]point, 0, n)
	x := -(n * 2)
	for i := int64(0); i < n; i++ {
		points = append(points, point{x, x * x})
		x += 1 + nextRandom(seed)%3
	}
	if dent {
		i := 1 + nextRandom(seed)%(n-2)
		xa, xb, yb, xc := points[i-1].x, points[i].x, points[i].y, points[i+1].x
		points[i] = point{xb, yb + (xb-xa)*(xc-xb) + 1}
	}
	return points
}

func main() {
	const count = 100
	const n = 50000
	const rounds = 20
	seed := int64(469)
	polygons := make([][]point, 0, count)
	for k := 0; k < count; k++ {
		polygons = append(polygons, polygon(n, k%2 == 1, &seed))
	}
	var convex, checksum int64
	for r := int64(0); r < rounds; r++ {
		for k := 0; k < count; k++ {
			answer := isConvex(polygons[k])
			code := int64(2)
			if answer {
				convex++
				code = 1
			}
			checksum = (checksum*3 + code + r) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d polygons of %d vertices: %d convex, checksum %d\n", rounds, count, n, convex, checksum)
}
