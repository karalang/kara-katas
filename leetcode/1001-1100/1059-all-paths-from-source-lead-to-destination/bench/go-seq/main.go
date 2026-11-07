// LeetCode #1059: All Paths from Source Lead to Destination -- the
// benchmark, the same algorithm as paths.kara.
package main

import "fmt"

const (
	unseen = 0
	onPath = 1
	done   = 2
)

type edge struct{ u, v int64 }
type frame struct{ node, next int64 }

func leadsToDestination(n int64, edges []edge, source, destination int64) bool {
	adj := make([][]int64, n)
	for _, e := range edges {
		adj[e.u] = append(adj[e.u], e.v)
	}
	state := make([]int64, n)
	stack := []frame{{source, 0}}
	state[source] = onPath
	for len(stack) > 0 {
		top := len(stack) - 1
		u, next := stack[top].node, stack[top].next
		if len(adj[u]) == 0 && u != destination {
			return false
		}
		if next == int64(len(adj[u])) {
			state[u] = done
			stack = stack[:top]
			continue
		}
		stack[top].next = next + 1
		v := adj[u][next]
		if state[v] == onPath {
			return false
		}
		if state[v] == unseen {
			state[v] = onPath
			stack = append(stack, frame{v, 0})
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func leaningGraph(n, perNode, back int64, seed *int64) []edge {
	var edges []edge
	for u := int64(0); u < n-1; u++ {
		k := nextRandom(seed) % (perNode + 1)
		for i := int64(0); i < k; i++ {
			span := n - 1 - u
			if span > 20 {
				span = 20
			}
			edges = append(edges, edge{u, u + 1 + nextRandom(seed)%span})
		}
		if k == 0 && nextRandom(seed)%4 != 0 {
			edges = append(edges, edge{u, n - 1})
		}
		if nextRandom(seed)%back == 0 {
			edges = append(edges, edge{u, nextRandom(seed) % (u + 1)})
		}
	}
	return edges
}

func main() {
	seed := int64(1059)
	n := int64(2000)
	var graphs [][]edge
	for g := 0; g < 20; g++ {
		graphs = append(graphs, leaningGraph(n, 2, 1000, &seed))
	}
	var calls, yes, check int64
	for _, edges := range graphs {
		for source := int64(0); source < n; source++ {
			answer := leadsToDestination(n, edges, source, n-1)
			add := int64(3)
			if answer {
				yes++
				add = 7 + source%13
			}
			check = (check*31 + add) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: %d lead, checksum %d\n", calls, yes, check)
}
