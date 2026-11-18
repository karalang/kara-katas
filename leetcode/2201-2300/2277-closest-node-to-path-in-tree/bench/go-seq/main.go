// LeetCode #2277: Closest Node to Path in Tree -- the bench, the ★ arm.
package main

import "fmt"

func distances(n int, adj [][]int, from int) []int64 {
	dist := make([]int64, n)
	for i := range dist {
		dist[i] = -1
	}
	dist[from] = 0
	queue := []int{from}
	for head := 0; head < len(queue); head++ {
		v := queue[head]
		for _, w := range adj[v] {
			if dist[w] < 0 {
				dist[w] = dist[v] + 1
				queue = append(queue, w)
			}
		}
	}
	return dist
}

func closestNode(n int, edges [][]int, query [][]int) []int {
	adj := make([][]int, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], e[1])
		adj[e[1]] = append(adj[e[1]], e[0])
	}
	dist := make([][]int64, n)
	for v := 0; v < n; v++ {
		dist[v] = distances(n, adj, v)
	}
	answer := make([]int, 0, len(query))
	for _, q := range query {
		start, end, node := q[0], q[1], q[2]
		best := start
		for u := 0; u < n; u++ {
			if dist[start][u]+dist[u][end] == dist[start][end] && dist[u][node] < dist[best][node] {
				best = u
			}
		}
		answer = append(answer, best)
	}
	return answer
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2277

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 50; t++ {
		edges := make([][]int, 0, 999)
		for i := 1; i < 1000; i++ {
			edges = append(edges, []int{i, int(nextRandom() % int64(i))})
		}
		query := make([][]int, 0, 1000)
		for i := 0; i < 1000; i++ {
			s := int(nextRandom() % 1000)
			e := int(nextRandom() % 1000)
			x := int(nextRandom() % 1000)
			query = append(query, []int{s, e, x})
		}
		for _, a := range closestNode(1000, edges, query) {
			check = (check*31 + int64(a)) % 1000000007
		}
	}
	fmt.Printf("50 trees of 1000: checksum %d\n", check)
}
