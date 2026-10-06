// Benchmark for #356 -- same workload and algorithm as line_reflection.kara.
package main

import "fmt"

type point struct{ x, y int64 }

func isReflected(points []point) bool {
	if len(points) == 0 {
		return true
	}
	lo := points[0].x
	hi := points[0].x
	seen := make(map[point]struct{})
	for _, p := range points {
		lo = min(lo, p.x)
		hi = max(hi, p.x)
		seen[p] = struct{}{}
	}
	sum := lo + hi
	for _, p := range points {
		if _, ok := seen[point{sum - p.x, p.y}]; !ok {
			return false
		}
	}
	return true
}

func main() {
	var seed int64 = 356
	yes := 0
	var checksum int64 = 0
	for round := 0; round < 400; round++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		center2 := (seed/16)%2000001 - 1000000
		points := make([]point, 0, 5000)
		for k := 0; k < 2500; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			x := (seed/16)%2000001 - 1000000
			seed = (seed*1103515245 + 12345) % 2147483648
			y := (seed / 65536) % 1000
			points = append(points, point{x, y}, point{center2 - x, y})
		}
		if round%3 == 0 {
			seed = (seed*1103515245 + 12345) % 2147483648
			i := (seed / 65536) % int64(len(points))
			points[i] = point{points[i].x + 1, points[i].y}
		}
		r := isReflected(points)
		if r {
			yes++
		}
		var bit int64 = 2
		if r {
			bit = 1
		}
		checksum = (checksum*3 + bit) % 1000000007
	}
	fmt.Printf("%d of 400 sets reflect, checksum %d\n", yes, checksum)
}
