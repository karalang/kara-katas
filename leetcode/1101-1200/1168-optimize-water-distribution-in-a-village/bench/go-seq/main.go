// LeetCode #1168: Optimize Water Distribution in a Village -- the ★ arm's
// bench in Go: Kruskal over the pipes and a pipe from a source to every
// house, union-find by size with path halving.
package main

import (
	"fmt"
	"sort"
)

type edge struct{ c, a, b int64 }

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func minCost(n int64, wells []int64, pipes [][]int64) int64 {
	edges := make([]edge, 0, int(n)+len(pipes))
	for i, w := range wells {
		edges = append(edges, edge{w, 0, int64(i) + 1})
	}
	for _, p := range pipes {
		edges = append(edges, edge{p[2], p[0], p[1]})
	}
	sort.Slice(edges, func(i, j int) bool {
		x, y := edges[i], edges[j]
		if x.c != y.c {
			return x.c < y.c
		}
		if x.a != y.a {
			return x.a < y.a
		}
		return x.b < y.b
	})
	parent := make([]int64, n+1)
	size := make([]int64, n+1)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	var cost, joined int64
	for _, e := range edges {
		ra, rb := find(parent, e.a), find(parent, e.b)
		if ra == rb {
			continue
		}
		if size[ra] < size[rb] {
			ra, rb = rb, ra
		}
		parent[rb] = ra
		size[ra] += size[rb]
		cost += e.c
		joined++
		if joined == n {
			break
		}
	}
	return cost
}

var seed int64 = 1168

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 10000
	wells := make([][]int64, 16)
	pipes := make([][][]int64, 16)
	for v := 0; v < 16; v++ {
		for i := 0; i < n; i++ {
			wells[v] = append(wells[v], nextRandom()%100001)
		}
		for j := 0; j < 10000; j++ {
			a := 1 + nextRandom()%n
			b := 1 + nextRandom()%(n-1)
			if b >= a {
				b++
			}
			pipes[v] = append(pipes[v], []int64{a, b, nextRandom() % 100001})
		}
	}
	var total, check int64
	for r := 0; r < 40; r++ {
		for v := 0; v < 16; v++ {
			j := nextRandom() % 10000
			pipes[v][j][2] = nextRandom() % 100001
			c := minCost(n, wells[v], pipes[v])
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("40 rounds over 16 villages of 10^4 houses: total %d, checksum %d\n", total, check)
}
