// LeetCode #1066: Campus Bikes II -- the benchmark, the same table over
// the sets of bikes taken as campus_bikes.kara.
package main

import (
	"fmt"
	"math"
	"math/bits"
)

type point struct{ x, y int64 }

func abs(a int64) int64 {
	if a < 0 {
		return -a
	}
	return a
}

func distance(a, b point) int64 { return abs(a.x-b.x) + abs(a.y-b.y) }

func assignBikes(workers, bikes []point) int64 {
	n, m := len(workers), len(bikes)
	best := make([]int64, 1<<m)
	for k := range best {
		best[k] = math.MaxInt64
	}
	best[0] = 0
	answer := int64(math.MaxInt64)
	for mask := 0; mask < len(best); mask++ {
		if best[mask] == math.MaxInt64 {
			continue
		}
		w := bits.OnesCount(uint(mask))
		if w == n {
			answer = min(answer, best[mask])
			continue
		}
		for b := 0; b < m; b++ {
			if mask&(1<<b) == 0 {
				next := mask | (1 << b)
				best[next] = min(best[next], best[mask]+distance(workers[w], bikes[b]))
			}
		}
	}
	return answer
}

var seed int64 = 1066

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPoints(n int64) []point {
	ps := make([]point, n)
	for i := range ps {
		x := nextRandom() % 1000
		ps[i] = point{x, nextRandom() % 1000}
	}
	return ps
}

func main() {
	// 5000 problems of 8 to 10 workers and 10 bikes on a 1000 by 1000
	// grid, built once, then each answered
	type problem struct{ workers, bikes []point }
	problems := []problem{}
	for p := 0; p < 5000; p++ {
		n := 8 + nextRandom()%3
		workers := randomPoints(n)
		problems = append(problems, problem{workers, randomPoints(10)})
	}
	var calls, total, check int64
	for _, p := range problems {
		answer := assignBikes(p.workers, p.bikes)
		total += answer
		check = (check*31 + answer) % 1000000007
		calls++
	}
	fmt.Printf("%d calls: answers sum %d, checksum %d\n", calls, total, check)
}
