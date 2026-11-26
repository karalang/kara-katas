// LeetCode #1761: Minimum Degree of a Connected Trio in a Graph -- the bench
// in Go, mirroring min_trio_degree.kara: an adjacency matrix, the degrees,
// and every edge (u, v) with each w above v.
package main

import (
	"fmt"
	"math"
)

func minTrioDegree(n int, edges [][]int32) int32 {
	joined := make([][]bool, n+1)
	for i := range joined {
		joined[i] = make([]bool, n+1)
	}
	degree := make([]int32, n+1)
	for _, e := range edges {
		u, v := e[0], e[1]
		joined[u][v] = true
		joined[v][u] = true
		degree[u]++
		degree[v]++
	}
	best := int32(math.MaxInt32)
	for u := 1; u <= n; u++ {
		for v := u + 1; v <= n; v++ {
			if !joined[u][v] {
				continue
			}
			for w := v + 1; w <= n; w++ {
				if joined[u][w] && joined[v][w] {
					best = min(best, degree[u]+degree[v]+degree[w]-6)
				}
			}
		}
	}
	if best == math.MaxInt32 {
		return -1
	}
	return best
}

type pair struct {
	u, v int32
	w    int64
}

func main() {
	seed := int64(1761)
	weights := make([]pair, 0, 400*399/2)
	for u := int32(1); u < 401; u++ {
		for v := u + 1; v < 401; v++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			weights = append(weights, pair{u, v, seed / 65536 % 1000})
		}
	}
	check := int64(0)
	for call := int64(0); call < 40; call++ {
		threshold := 300 + (check+call*7919)%500
		edges := [][]int32{}
		for _, p := range weights {
			if p.w < threshold {
				edges = append(edges, []int32{p.u, p.v})
			}
		}
		check = (check*31 + int64(minTrioDegree(400, edges)) + 1) % 1000000007
	}
	fmt.Printf("40 calls on 400 nodes: checksum %d\n", check)
}
