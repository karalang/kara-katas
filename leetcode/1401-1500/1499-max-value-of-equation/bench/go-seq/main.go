// LeetCode #1499: Max Value of Equation -- the bench in Go, mirroring
// find_max_value_of_equation.kara: a window of (y - x, x) kept largest first,
// here a slice used as a deque.
package main

import (
	"fmt"
	"math"
)

type entry struct{ v, x int32 }

func findMaxValueOfEquation(points [][]int32, k int32) int32 {
	window := make([]entry, 0, len(points))
	head := 0
	best := int32(math.MinInt32)
	for _, p := range points {
		x, y := p[0], p[1]
		for head < len(window) && x-window[head].x > k {
			head++
		}
		if head < len(window) {
			best = max(best, window[head].v+y+x)
		}
		for head < len(window) && window[len(window)-1].v <= y-x {
			window = window[:len(window)-1]
		}
		window = append(window, entry{y - x, x})
	}
	return best
}

func main() {
	seed := int64(1499)
	points := make([][]int32, 0, 200000)
	x := int64(0)
	for i := 0; i < 200000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		x += 1 + seed/65536%10
		seed = (seed*1103515245 + 12345) % 2147483648
		y := seed/65536*6151%200000001 - 100000000
		points = append(points, []int32{int32(x), int32(y)})
	}
	check := int64(0)
	for call := int64(0); call < 400; call++ {
		at := (check + call*7919) % 200000
		points[at][1] = int32((check*17+call)%200000001 - 100000000)
		k := 10 + (check+call)%2000
		check = (check*31 + int64(findMaxValueOfEquation(points, int32(k))) + 300000000) % 1000000007
	}
	fmt.Printf("400 calls over 200000 points: checksum %d\n", check)
}
