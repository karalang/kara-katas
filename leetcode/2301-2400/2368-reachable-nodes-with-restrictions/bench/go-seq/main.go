// LeetCode #2368: Reachable Nodes With Restrictions -- the bench, the ★
// arm in Go: adjacency lists, the restricted nodes marked, and a
// breadth-first search from node 0 that never enters a marked node.
package main

import "fmt"

type edge struct{ a, b int }

func reachableNodes(n int, edges []edge, restricted []int) int64 {
	next := make([][]int, n)
	for _, e := range edges {
		next[e.a] = append(next[e.a], e.b)
		next[e.b] = append(next[e.b], e.a)
	}
	seen := make([]bool, n)
	for _, r := range restricted {
		seen[r] = true
	}
	seen[0] = true
	queue := []int{0}
	for head := 0; head < len(queue); head++ {
		u := queue[head]
		for _, v := range next[u] {
			if !seen[v] {
				seen[v] = true
				queue = append(queue, v)
			}
		}
	}
	return int64(len(queue))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type tree struct {
	edges      []edge
	restricted []int
}

func main() {
	// tree a: 10^5 nodes, node i joined to one of the 4^a nodes before it,
	// and each node but 0 restricted with a chance of 1 in 2^(a + 4)
	n := 100000
	seed := int64(2368)
	trees := make([]tree, 0, 10)
	width := int64(1)
	for a := 0; a < 10; a++ {
		edges := make([]edge, 0, n-1)
		for i := 1; i < n; i++ {
			edges = append(edges, edge{i - 1 - int(nextRandom(&seed)%min(width, int64(i))), i})
		}
		restricted := []int{}
		for i := 1; i < n; i++ {
			if nextRandom(&seed)%(int64(16)<<a) == 0 {
				restricted = append(restricted, i)
			}
		}
		trees = append(trees, tree{edges, restricted})
		width *= 4
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, t := range trees {
			check = (check*31 + reachableNodes(n, t.edges, t.restricted) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 trees of 10^5 nodes: checksum %d\n", check)
}
