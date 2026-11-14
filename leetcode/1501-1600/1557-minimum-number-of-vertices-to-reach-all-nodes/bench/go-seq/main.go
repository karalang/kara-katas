// LeetCode #1557: Minimum Number of Vertices to Reach All Nodes -- bench:
// the ★ arm (the nodes no edge ends at) over 20 acyclic graphs of 100000
// nodes and up to 300000 edges, built once, each asked 20 times. Go mirror of vertices.kara.
package main

import "fmt"

type edge struct{ from, to int64 }

func findSmallestSetOfVertices(n int64, edges []edge) []int64 {
	reached := make([]bool, n)
	for _, e := range edges {
		reached[e.to] = true
	}
	sources := []int64{}
	for v := int64(0); v < n; v++ {
		if !reached[v] {
			sources = append(sources, v)
		}
	}
	return sources
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	n := int64(100000)
	seed := int64(1557)
	graphs := [][]edge{}
	for g := 0; g < 20; g++ {
		order := make([]int64, n)
		for i := range order {
			order[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := (nextRandom(&seed)*32768 + nextRandom(&seed)) % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		edges := []edge{}
		for e := 0; e < 300000; e++ {
			a := (nextRandom(&seed)*32768 + nextRandom(&seed)) % n
			b := (nextRandom(&seed)*32768 + nextRandom(&seed)) % n
			if a < b {
				edges = append(edges, edge{order[a], order[b]})
			}
		}
		graphs = append(graphs, edges)
	}
	check, total := int64(0), 0
	for pass := 0; pass < 20; pass++ {
		for g := range graphs {
			sources := findSmallestSetOfVertices(n, graphs[g])
			total += len(sources)
			check = mix(check, sources[(pass*7+g)%len(sources)])
		}
	}
	fmt.Printf("20 passes over 20 graphs of 100000 nodes: %d sources, checksum %d\n", total, check)
}
