// LeetCode #2065: Maximum Path Quality of a Graph -- Go mirror of the ★
// arm's benchmark (quality.kara): 1000 graphs of 1000 nodes, 2000 edges
// tried, each from a node to one of the next three and of time 10 or 11,
// and the time 100; a recursive search with a count of visits per node.
package main

import "fmt"

type edge struct {
	to int
	t  int64
}

func walk(adj [][]edge, values []int64, maxTime int64, node int, time, quality int64, visits []int64, best *int64) {
	if node == 0 && quality > *best {
		*best = quality
	}
	for _, e := range adj[node] {
		if time+e.t <= maxTime {
			visits[e.to]++
			gain := int64(0)
			if visits[e.to] == 1 {
				gain = values[e.to]
			}
			walk(adj, values, maxTime, e.to, time+e.t, quality+gain, visits, best)
			visits[e.to]--
		}
	}
}

var seed int64 = 2065

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	total, check := int64(0), int64(0)
	for g := 0; g < 1000; g++ {
		n := 1000
		values := make([]int64, n)
		for i := range values {
			hi := nextRandom()
			values[i] = (hi*32768 + nextRandom()) % 100000001
		}
		degree := make([]int, n)
		seen := map[[2]int]bool{}
		adj := make([][]edge, n)
		for e := 0; e < 2000; e++ {
			u := int(nextRandom() % int64(n))
			v := (u + 1 + int(nextRandom()%3)) % n
			t := nextRandom()%2 + 10
			key := [2]int{min(u, v), max(u, v)}
			if degree[u] < 4 && degree[v] < 4 && !seen[key] {
				seen[key] = true
				degree[u]++
				degree[v]++
				adj[u] = append(adj[u], edge{v, t})
				adj[v] = append(adj[v], edge{u, t})
			}
		}
		visits := make([]int64, n)
		visits[0] = 1
		best := int64(0)
		walk(adj, values, 100, 0, 0, values[0], visits, &best)
		total += best
		check = (check*31 + best%1000000007) % 1000000007
	}
	fmt.Printf("1000 graphs: sum %d, checksum %d\n", total, check)
}
