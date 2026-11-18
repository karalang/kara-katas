// LeetCode #2316: Count Unreachable Pairs of Nodes in an Undirected
// Graph -- the bench, the ★ arm in Go. Union-find with union by size and
// path halving, then each set's root, met in order, pairs its size with
// every node of the sets before it.
package main

import "fmt"

type edge struct{ a, b int64 }

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func countPairs(n int64, edges []edge) int64 {
	parent := make([]int64, n)
	size := make([]int64, n)
	for x := int64(0); x < n; x++ {
		parent[x] = x
		size[x] = 1
	}
	for _, e := range edges {
		ra := find(parent, e.a)
		rb := find(parent, e.b)
		if ra != rb {
			if size[ra] < size[rb] {
				ra, rb = rb, ra
			}
			parent[rb] = ra
			size[ra] += size[rb]
		}
	}
	var before, pairs int64
	for x := int64(0); x < n; x++ {
		if parent[x] == x {
			pairs += size[x] * before
			before += size[x]
		}
	}
	return pairs
}

var seed int64 = 2316

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	graphs := make([][]edge, 0, 10)
	for g := int64(0); g < 10; g++ {
		var edges []edge
		for i := int64(1); i < n; i++ {
			if nextRandom()%(g+3) != 0 {
				hi := nextRandom()
				j := (hi*32768 + nextRandom()) % i
				edges = append(edges, edge{i, j})
			}
		}
		graphs = append(graphs, edges)
	}
	var check int64
	for p := 0; p < 50; p++ {
		for a := 0; a < 10; a++ {
			check = (check*31 + countPairs(n, graphs[(a+p)%10])%1000000007) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 graphs of 10^5 nodes: checksum %d\n", check)
}
