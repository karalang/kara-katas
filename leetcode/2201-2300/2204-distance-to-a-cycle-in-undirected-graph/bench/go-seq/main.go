// benchmark's Go mirror of cycle.kara (LeetCode #2204, the ★ arm): leaves
// peeled by degree, then one breadth-first search from the cycle.
package main

import "fmt"

func distanceToCycle(n int64, edges [][2]int64) []int64 {
	adj := make([][]int64, n)
	degree := make([]int64, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], e[1])
		adj[e[1]] = append(adj[e[1]], e[0])
		degree[e[0]]++
		degree[e[1]]++
	}
	leaves := []int64{}
	for v := int64(0); v < n; v++ {
		if degree[v] == 1 {
			leaves = append(leaves, v)
		}
	}
	peeled := make([]bool, n)
	for head := 0; head < len(leaves); head++ {
		v := leaves[head]
		peeled[v] = true
		for _, u := range adj[v] {
			degree[u]--
			if degree[u] == 1 {
				leaves = append(leaves, u)
			}
		}
	}
	dist := make([]int64, n)
	frontier := []int64{}
	for v := int64(0); v < n; v++ {
		dist[v] = -1
		if !peeled[v] {
			dist[v] = 0
			frontier = append(frontier, v)
		}
	}
	for head := 0; head < len(frontier); head++ {
		v := frontier[head]
		for _, u := range adj[v] {
			if dist[u] < 0 {
				dist[u] = dist[v] + 1
				frontier = append(frontier, u)
			}
		}
	}
	return dist
}

var seed int64 = 2204

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func randomGraph(n, ring int64) [][2]int64 {
	order := make([]int64, n)
	for i := range order {
		order[i] = int64(i)
	}
	for i := n - 1; i > 0; i-- {
		j := wideRandom() % (i + 1)
		order[i], order[j] = order[j], order[i]
	}
	edges := [][2]int64{}
	for i := int64(0); i < ring; i++ {
		edges = append(edges, [2]int64{order[i], order[(i+1)%ring]})
	}
	for i := ring; i < n; i++ {
		edges = append(edges, [2]int64{order[i], order[wideRandom()%i]})
	}
	for i := n - 1; i > 0; i-- {
		j := wideRandom() % (i + 1)
		edges[i], edges[j] = edges[j], edges[i]
	}
	for i := range edges {
		if nextRandom()%2 == 1 {
			edges[i][0], edges[i][1] = edges[i][1], edges[i][0]
		}
	}
	return edges
}

func main() {
	graphs := [][][2]int64{}
	for _, ring := range []int64{3, 10, 100, 1000, 10000, 100000} {
		graphs = append(graphs, randomGraph(100000, ring))
	}
	var check int64
	for pass := 0; pass < 5; pass++ {
		for _, edges := range graphs {
			dist := distanceToCycle(100000, edges)
			var sum int64
			for _, d := range dist {
				sum += d
			}
			check = (check*31 + sum + dist[len(dist)/2]) % 1000000007
		}
	}
	fmt.Printf("5 passes over 6 graphs: checksum %d\n", check)
}
