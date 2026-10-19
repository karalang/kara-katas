// LeetCode 802 -- Find Eventual Safe States: the bench, mirroring
// eventual_safe_nodes.kara with the same three-colour search.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 802

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func isSafe(graph [][]int64, node int64, colour []int64) bool {
	if colour[node] != 0 {
		return colour[node] == 2
	}
	colour[node] = 1
	for _, next := range graph[node] {
		if !isSafe(graph, next, colour) {
			return false
		}
	}
	colour[node] = 2
	return true
}

func eventualSafeNodes(graph [][]int64) []int64 {
	n := int64(len(graph))
	// 0 not seen yet, 1 grey (on the search or unsafe), 2 black (safe).
	colour := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		colour = append(colour, 0)
	}
	safe := make([]int64, 0)
	for node := int64(0); node < n; node++ {
		if isSafe(graph, node, colour) {
			safe = append(safe, node)
		}
	}
	return safe
}

func main() {
	var n int64 = 10000
	graphs := make([][][]int64, 0)
	for g := 0; g < 16; g++ {
		graph := make([][]int64, 0)
		for a := int64(0); a < n; a++ {
			picked := make([]int64, 0)
			edges := nextRandom() % 5
			for e := int64(0); e < edges; e++ {
				var b int64
				if nextRandom()%1000 == 0 {
					b = a - 1 - nextRandom()%50
					if b < 0 {
						b = 0
					}
				} else {
					b = a + 1 + nextRandom()%50
				}
				if b < n {
					picked = append(picked, b)
				}
			}
			// In increasing order with no edge twice, as LeetCode gives.
			sort.Slice(picked, func(i, j int) bool { return picked[i] < picked[j] })
			out := make([]int64, 0)
			for _, b := range picked {
				if len(out) == 0 || out[len(out)-1] != b {
					out = append(out, b)
				}
			}
			graph = append(graph, out)
		}
		graphs = append(graphs, graph)
	}
	var rounds int64 = 4000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		safe := eventualSafeNodes(graphs[r%16])
		count := int64(len(safe))
		total += count
		check = (check*131 + count + safe[len(safe)/2]) % 1000000007
	}
	fmt.Printf("%d rounds of %d nodes: %d safe nodes in all, checksum %d\n", rounds, n, total, check)
}
