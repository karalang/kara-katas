// Benchmark: LeetCode #973 K Closest Points to Origin -- the ★ arm, sort
// by squared distance, on 100 sets of 1000 random points. Mirrors
// k_closest.kara, .rs, .c and .py.
package main

import (
	"fmt"
	"sort"
)

type point struct{ x, y int64 }

func kClosest(points []point, k int) []point {
	sorted := append([]point(nil), points...)
	sort.Slice(sorted, func(i, j int) bool {
		a, b := sorted[i], sorted[j]
		return a.x*a.x+a.y*a.y < b.x*b.x+b.y*b.y
	})
	return sorted[:k]
}

var seed int64 = 973

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomCase(n int) ([]point, int) {
	points := make([]point, n)
	ds := make([]int64, n)
	for i := range points {
		x := nextRandom()%20001 - 10000
		y := nextRandom()%20001 - 10000
		points[i] = point{x, y}
		ds[i] = x*x + y*y
	}
	sort.Slice(ds, func(i, j int) bool { return ds[i] < ds[j] })
	k := 1 + int(nextRandom()%int64(n))
	for k < n && ds[k-1] == ds[k] {
		k++
	}
	return points, k
}

func main() {
	rounds, count := 100, 100
	type kase struct {
		points []point
		k      int
	}
	cases := make([]kase, count)
	for c := range cases {
		p, k := randomCase(1000)
		cases[c] = kase{p, k}
	}
	kept := 0
	var check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			c := cases[(r+i)%count]
			answer := kClosest(c.points, c.k)
			kept += len(answer)
			for _, p := range answer {
				v := ((p.x+10001)*20003 + p.y + 10001) % 1000000007
				check = (check + v*v) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d sets of 1000 points: %d points kept, checksum %d\n", rounds, count, kept, check)
}
