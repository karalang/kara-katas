// LeetCode #882 bench: Go mirror of reachable_nodes.kara (the ★ arm,
// Dijkstra with a priority queue) on the same 600 graphs.
package main

import (
	"container/heap"
	"fmt"
	"slices"
)

type entry struct{ d, u int64 }

type minHeap []entry

func (h minHeap) Len() int { return len(h) }
func (h minHeap) Less(i, j int) bool {
	return h[i].d < h[j].d || (h[i].d == h[j].d && h[i].u < h[j].u)
}
func (h minHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)   { *h = append(*h, x.(entry)) }
func (h *minHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func reachableNodes(edges [][]int64, maxMoves, n int64) int64 {
	adj := make([][]int, n)
	for e, edge := range edges {
		adj[edge[0]] = append(adj[edge[0]], e)
		adj[edge[1]] = append(adj[edge[1]], e)
	}
	dist := make([]int64, n)
	for u := range dist {
		dist[u] = maxMoves + 1
	}
	dist[0] = 0
	queue := &minHeap{{0, 0}}
	for queue.Len() > 0 {
		top := heap.Pop(queue).(entry)
		d, u := top.d, top.u
		if d > dist[u] {
			continue
		}
		for _, e := range adj[u] {
			v := edges[e][0] + edges[e][1] - u
			next := d + edges[e][2] + 1
			if next < dist[v] {
				dist[v] = next
				heap.Push(queue, entry{next, v})
			}
		}
	}
	var seen int64
	for u := int64(0); u < n; u++ {
		if dist[u] <= maxMoves {
			seen++
		}
	}
	for _, edge := range edges {
		fromU := max(maxMoves-dist[edge[0]], 0)
		fromV := max(maxMoves-dist[edge[1]], 0)
		seen += min(fromU+fromV, edge[2])
	}
	return seen
}

var seed int64 = 882

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(limit int64) int64 {
	x := nextRandom()
	y := nextRandom()
	return (x*32768 + y) % limit
}

func main() {
	var total, check int64
	for k := 0; k < 600; k++ {
		n := 2000 + below(1001)
		offsets := make([]int64, 0, 3)
		for len(offsets) < 3 {
			d := 1 + below(n/2-1)
			if !slices.Contains(offsets, d) {
				offsets = append(offsets, d)
			}
		}
		edges := make([][]int64, 0, 3*n)
		for u := int64(0); u < n; u++ {
			for j := 0; j < 3; j++ {
				edges = append(edges, []int64{u, (u + offsets[j]) % n, below(10001)})
			}
		}
		maxMoves := below(200000)
		reached := reachableNodes(edges, maxMoves, n)
		total += reached
		check = (check*131 + reached) % 1000000007
	}
	fmt.Printf("600 graphs of up to 3000 nodes: %d nodes reached, checksum %d\n", total, check)
}
