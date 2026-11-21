// LeetCode #2492: Minimum Score of a Path Between Two Cities -- Go mirror
// of the benchmark (score.kara): the same map, passes and checksum, the
// breadth-first search over adjacency slices built on every ask.
package main

import (
	"fmt"
	"math"
)

var seed int64 = 2492

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type edge struct{ to, distance int64 }

func minScore(n int64, roads [][3]int64) int64 {
	next := make([][]edge, n+1)
	for _, r := range roads {
		next[r[0]] = append(next[r[0]], edge{r[1], r[2]})
		next[r[1]] = append(next[r[1]], edge{r[0], r[2]})
	}
	seen := make([]bool, n+1)
	queue := []int64{1}
	seen[1] = true
	head := 0
	least := int64(math.MaxInt64)
	for head < len(queue) {
		city := queue[head]
		head++
		for _, e := range next[city] {
			if e.distance < least {
				least = e.distance
			}
			if !seen[e.to] {
				seen[e.to] = true
				queue = append(queue, e.to)
			}
		}
	}
	return least
}

func main() {
	const n int64 = 100000
	const passes int64 = 50
	roads := [][3]int64{{1, n, 10000}}
	for int64(len(roads)) < n {
		a := (nextRandom()*32768+nextRandom())%n + 1
		b := (nextRandom()*32768+nextRandom())%n + 1
		if a != b {
			roads = append(roads, [3]int64{a, b, nextRandom()%10000 + 1})
		}
	}
	m := int64(len(roads))
	var check int64
	for p := int64(0); p < passes; p++ {
		at := check % m
		was := roads[at][2]
		roads[at][2] = (check/m+p)%10000 + 1
		check = (check*31 + minScore(n, roads) + p) % 1000000007
		roads[at][2] = was
	}
	fmt.Printf("%d passes over 10^5 cities and %d roads: checksum %d\n", passes, m, check)
}
