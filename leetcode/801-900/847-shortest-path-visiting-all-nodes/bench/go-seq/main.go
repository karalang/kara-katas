// Benchmark for #847: Shortest Path Visiting All Nodes -- Go twin of the
// Kāra ★ arm (breadth-first search over (visited set, node) states).
package main

import "fmt"

type state struct{ mask, v, steps int64 }

func shortestPathLength(graph [][]int64) int64 {
	n := int64(len(graph))
	all := int64(1)<<n - 1
	seen := make([]bool, n<<n)
	// every state is queued at most once, so a slice with a head index is the queue
	queue := make([]state, 0, n)
	head := 0
	for v := int64(0); v < n; v++ {
		seen[(int64(1)<<v)*n+v] = true
		queue = append(queue, state{int64(1) << v, v, 0})
	}
	for head < len(queue) {
		s := queue[head]
		head++
		if s.mask == all {
			return s.steps
		}
		for _, w := range graph[s.v] {
			next := s.mask | int64(1)<<w
			if !seen[next*n+w] {
				seen[next*n+w] = true
				queue = append(queue, state{next, w, s.steps + 1})
			}
		}
	}
	return 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 4000, 12
	var seed int64 = 847
	graphs := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		edge := make([]bool, n*n)
		for v := int64(1); v < n; v++ {
			w := nextRandom(&seed) % v
			edge[v*n+w] = true
			edge[w*n+v] = true
		}
		for e := 0; e < g%16*3; e++ {
			v := nextRandom(&seed) % n
			w := nextRandom(&seed) % n
			if v != w {
				edge[v*n+w] = true
				edge[w*n+v] = true
			}
		}
		graph := make([][]int64, n)
		for v := int64(0); v < n; v++ {
			for w := int64(0); w < n; w++ {
				if edge[v*n+w] {
					graph[v] = append(graph[v], w)
				}
			}
		}
		graphs = append(graphs, graph)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		length := shortestPathLength(graphs[round%count])
		total += length
		checksum = (checksum*31 + length) % 1000000007
	}
	fmt.Printf("%d rounds of %d graphs: lengths sum to %d, checksum %d\n", rounds, count, total, checksum)
}
