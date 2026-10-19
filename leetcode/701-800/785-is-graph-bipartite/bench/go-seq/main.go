// LeetCode 785 — Is Graph Bipartite?: the bench, in Go.
// Mirrors is_bipartite.kara: two colours by breadth first search over the
// same 64 graphs, with a slice as the queue.
package main

import "fmt"

func isBipartite(graph [][]int64) bool {
	n := len(graph)
	colour := make([]int64, n)
	for i := range colour {
		colour[i] = -1
	}
	queue := []int64{}
	for start := 0; start < n; start++ {
		if colour[start] != -1 {
			continue
		}
		colour[start] = 0
		queue = append(queue[:0], int64(start))
		for len(queue) > 0 {
			u := queue[0]
			queue = queue[1:]
			for _, v := range graph[u] {
				if colour[v] == -1 {
					colour[v] = 1 - colour[u]
					queue = append(queue, v)
				} else if colour[v] == colour[u] {
					return false
				}
			}
		}
	}
	return true
}

var seed int64 = 785

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	graphs := make([][][]int64, 0, 64)
	for g := 0; g < 64; g++ {
		side := make([]int64, 100)
		for i := range side {
			side[i] = nextRandom() % 2
		}
		graph := make([][]int64, 100)
		for a := 0; a < 100; a++ {
			for b := a + 1; b < 100; b++ {
				if side[a] != side[b] && nextRandom()%10 == 0 {
					graph[a] = append(graph[a], int64(b))
					graph[b] = append(graph[b], int64(a))
				}
			}
		}
		if g%2 == 1 {
			a := nextRandom() % 100
			b := (a + 1) % 100
			for side[b] != side[a] {
				b = (b + 1) % 100
			}
			graph[a] = append(graph[a], b)
			graph[b] = append(graph[b], a)
		}
		graphs = append(graphs, graph)
	}
	const rounds int64 = 500000
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		answer := isBipartite(graphs[r%64])
		v := int64(1)
		if answer {
			yes++
			v = 2
		}
		check = (check*31 + v + r%7) % 1000000007
	}
	fmt.Printf("%d rounds of 100-node graphs: %d bipartite, checksum %d\n", rounds, yes, check)
}
