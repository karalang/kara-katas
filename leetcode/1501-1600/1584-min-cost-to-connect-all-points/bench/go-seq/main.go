// LeetCode #1584 bench: the same Prim's algorithm with no edge list, in Go.
package main

import (
	"fmt"
	"math"
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func minCostConnectPoints(points [][]int64) int64 {
	n := len(points)
	nearest := make([]int64, n)
	inside := make([]bool, n)
	for i := range nearest {
		nearest[i] = math.MaxInt64
	}
	nearest[0] = 0
	var cost int64
	for k := 0; k < n; k++ {
		next := -1
		for i := 0; i < n; i++ {
			if !inside[i] && (next < 0 || nearest[i] < nearest[next]) {
				next = i
			}
		}
		inside[next] = true
		cost += nearest[next]
		for i := 0; i < n; i++ {
			if !inside[i] {
				d := abs(points[i][0]-points[next][0]) + abs(points[i][1]-points[next][1])
				nearest[i] = min(nearest[i], d)
			}
		}
	}
	return cost
}

var seed int64 = 1584

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	problems := make([][][]int64, 0, 100)
	for p := 0; p < 100; p++ {
		seen := map[[2]int64]bool{}
		points := make([][]int64, 0)
		for len(points) < 1000 {
			x := (nextRandom()*32768+nextRandom())%2000001 - 1000000
			y := (nextRandom()*32768+nextRandom())%2000001 - 1000000
			if !seen[[2]int64{x, y}] {
				seen[[2]int64{x, y}] = true
				points = append(points, []int64{x, y})
			}
		}
		problems = append(problems, points)
	}
	var check, total int64
	for _, pts := range problems {
		cost := minCostConnectPoints(pts)
		total += cost
		check = mix(check, cost)
	}
	fmt.Printf("100 problems of 1000 points: cost %d, checksum %d\n", total, check)
}
