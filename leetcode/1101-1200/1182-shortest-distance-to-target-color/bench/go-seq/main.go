// LeetCode #1182: Shortest Distance to Target Color -- the ★ arm in Go: a
// nearest-distance table per colour, filled from each side, then a lookup a
// query.
package main

import "fmt"

func shortestDistanceColor(colors []int64, queries [][]int64) []int64 {
	n := int64(len(colors))
	far := n + 1
	nearest := make([][]int64, 0, 3)
	for c := int64(1); c <= 3; c++ {
		dist := make([]int64, n)
		for i := range dist {
			dist[i] = far
		}
		last := int64(-1)
		for i := int64(0); i < n; i++ {
			if colors[i] == c {
				last = i
			}
			if last >= 0 {
				dist[i] = i - last
			}
		}
		last = -1
		for i := n - 1; i >= 0; i-- {
			if colors[i] == c {
				last = i
			}
			if last >= 0 && last-i < dist[i] {
				dist[i] = last - i
			}
		}
		nearest = append(nearest, dist)
	}
	answer := make([]int64, 0)
	for _, q := range queries {
		d := nearest[q[1]-1][q[0]]
		if d == far {
			d = -1
		}
		answer = append(answer, d)
	}
	return answer
}

var seed int64 = 1182

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 4)
	asks := make([][][]int64, 0, 4)
	for a := 0; a < 4; a++ {
		colors := make([]int64, 50000)
		for i := range colors {
			if nextRandom()%997 == 0 {
				colors[i] = 3
			} else {
				colors[i] = 1 + nextRandom()%2
			}
		}
		arrays = append(arrays, colors)
		queries := make([][]int64, 50000)
		for k := range queries {
			i := nextRandom() % 50000
			queries[k] = []int64{i, 1 + nextRandom()%3}
		}
		asks = append(asks, queries)
	}
	rounds := int64(40)
	check := int64(0)
	for round := int64(0); round < rounds; round++ {
		for a := 0; a < 4; a++ {
			for _, d := range shortestDistanceColor(arrays[a], asks[a]) {
				check = (check*131 + d + 2 + round) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds of 4 arrays of 50000 queries: checksum %d\n", rounds, check)
}
