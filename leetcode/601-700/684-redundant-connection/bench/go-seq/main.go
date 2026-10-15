// LeetCode #684: Redundant Connection -- union-find. Bench.
//
// 100 random trees of 20,000 vertices, each with one more edge, are
// built once; then 30 rounds answer every graph.
package main

import "fmt"

type edge struct{ a, b int64 }

func find(parent []int64, x int64) int64 {
	v := x
	for parent[v] != v {
		parent[v] = parent[parent[v]]
		v = parent[v]
	}
	return v
}

func findRedundantConnection(edges []edge) edge {
	n := int64(len(edges))
	parent := make([]int64, n+1)
	size := make([]int64, n+1)
	for v := int64(0); v <= n; v++ {
		parent[v] = v
		size[v] = 1
	}
	for _, e := range edges {
		ra := find(parent, e.a)
		rb := find(parent, e.b)
		if ra == rb {
			return e
		}
		if size[ra] < size[rb] {
			parent[ra] = rb
			size[rb] += size[ra]
		} else {
			parent[rb] = ra
			size[ra] += size[rb]
		}
	}
	return edge{0, 0}
}

var seed int64 = 684

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds int64 = 100, 20000, 30
	graphs := make([][]edge, 0, count)
	for c := int64(0); c < count; c++ {
		name := make([]int64, n)
		for v := int64(0); v < n; v++ {
			name[v] = v + 1
		}
		for i := n - 1; i > 0; i-- {
			j := nextRandom() % (i + 1)
			name[i], name[j] = name[j], name[i]
		}
		up := make([]int64, n)
		edges := make([]edge, 0, n)
		for v := int64(1); v < n; v++ {
			up[v] = nextRandom() % v
			edges = append(edges, edge{name[up[v]], name[v]})
		}
		for {
			x := nextRandom() % n
			y := nextRandom() % n
			lo, hi := x, y
			if y < x {
				lo, hi = y, x
			}
			if lo != hi && up[hi] != lo {
				edges = append(edges, edge{name[lo], name[hi]})
				break
			}
		}
		for k := n - 1; k > 0; k-- {
			j := nextRandom() % (k + 1)
			edges[k], edges[j] = edges[j], edges[k]
		}
		for e := int64(0); e < n; e++ {
			if nextRandom()%2 == 0 {
				edges[e] = edge{edges[e].b, edges[e].a}
			}
		}
		graphs = append(graphs, edges)
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for c := int64(0); c < count; c++ {
			e := findRedundantConnection(graphs[c])
			sum = (sum*31 + e.a*20011 + e.b + r) % 1000000007
		}
	}
	fmt.Printf("%d graphs answered, checksum %d\n", count*rounds, sum)
}
