// LeetCode #1245 bench, in Go: the ★ arm (two breadth-first searches over
// an adjacency list, a slice used as the queue) on 100 random trees of
// 10000 nodes built once, each asked 5 times; every diameter folded into a
// checksum.
package main

import "fmt"

func farthest(adj [][]int64, from int64) (int64, int64) {
	dist := make([]int64, len(adj))
	for i := range dist {
		dist[i] = -1
	}
	queue := []int64{from}
	dist[from] = 0
	last := from
	for head := 0; head < len(queue); head++ {
		node := queue[head]
		last = node
		for _, next := range adj[node] {
			if dist[next] < 0 {
				dist[next] = dist[node] + 1
				queue = append(queue, next)
			}
		}
	}
	return last, dist[last]
}

func treeDiameter(edges [][]int64) int64 {
	n := len(edges) + 1
	adj := make([][]int64, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], e[1])
		adj[e[1]] = append(adj[e[1]], e[0])
	}
	end, _ := farthest(adj, 0)
	_, diameter := farthest(adj, end)
	return diameter
}

var seed int64 = 1245

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func min(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func randomTree(n, shape int64) [][]int64 {
	label := make([]int64, n)
	for i := range label {
		label[i] = int64(i)
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % (i + 1)
		label[i], label[j] = label[j], label[i]
	}
	edges := make([][]int64, 0, n-1)
	for v := int64(1); v < n; v++ {
		var parent int64
		switch shape {
		case 0:
			parent = nextRandom() % v
		case 1:
			parent = v - 1 - nextRandom()%min(v, 3)
		default:
			parent = nextRandom() % min(v, 4)
		}
		edges = append(edges, []int64{label[parent], label[v]})
	}
	return edges
}

func main() {
	trees := make([][][]int64, 0, 100)
	for t := int64(0); t < 100; t++ {
		trees = append(trees, randomTree(10000, t%3))
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, edges := range trees {
			check = (check*131 + treeDiameter(edges)) % 1000000007
		}
	}
	fmt.Printf("5 rounds of 100 trees of 10000 nodes: checksum %d\n", check)
}
