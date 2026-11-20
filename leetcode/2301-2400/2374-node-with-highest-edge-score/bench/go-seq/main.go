// LeetCode #2374: Node With Highest Edge Score -- the bench, the ★ arm in
// Go: each node adds its label to the score of the node its edge points
// to, and the answer is the highest score's node, the smallest on a tie.
package main

import "fmt"

func edgeScore(edges []int) int64 {
	n := len(edges)
	score := make([]int64, n)
	for i := 0; i < n; i++ {
		score[edges[i]] += int64(i)
	}
	best := 0
	for v := 1; v < n; v++ {
		if score[v] > score[best] {
			best = v
		}
	}
	return int64(best)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// graph a: 10^5 nodes, each edge to one of the first 4^(a + 1) nodes
	// (at most all of them), another node than its own
	n := 100000
	seed := int64(2374)
	graphs := make([][]int, 0, 10)
	width := int64(4)
	for a := 0; a < 10; a++ {
		edges := make([]int, n)
		for i := range edges {
			hi := nextRandom(&seed)
			e := int((hi*32768 + nextRandom(&seed)) % min(width, int64(n)))
			if e == i {
				e = (e + 1) % n
			}
			edges[i] = e
		}
		graphs = append(graphs, edges)
		width *= 4
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, edges := range graphs {
			check = (check*31 + edgeScore(edges) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 graphs of 10^5 nodes: checksum %d\n", check)
}
