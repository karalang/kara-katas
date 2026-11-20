// LeetCode #1697: Checking Existence of Edge Length Limited Paths -- the
// bench's Go mirror: the ★ arm on 10 random graphs of 100000 nodes, 100000
// edges and 100000 queries, lengths and limits up to 10^9, all drawn
// first, each answered 5 times.
package main

import (
	"fmt"
	"slices"
)

func find(parent []int64, x int64) int64 {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	for parent[x] != root {
		next := parent[x]
		parent[x] = root
		x = next
	}
	return root
}

func distanceLimitedPathsExist(n int32, edgeList [][3]int32, queries [][3]int32) []bool {
	edges := slices.Clone(edgeList)
	slices.SortFunc(edges, func(a, b [3]int32) int { return int(a[2]) - int(b[2]) })
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	slices.SortFunc(order, func(a, b int) int { return int(queries[a][2]) - int(queries[b][2]) })
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
	}
	answer := make([]bool, len(queries))
	joined := 0
	for _, i := range order {
		limit := queries[i][2]
		for joined < len(edges) && edges[joined][2] < limit {
			a := find(parent, int64(edges[joined][0]))
			b := find(parent, int64(edges[joined][1]))
			parent[a] = b
			joined++
		}
		answer[i] = find(parent, int64(queries[i][0])) == find(parent, int64(queries[i][1]))
	}
	return answer
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1697

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide(bound int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % bound
}

func triples(count, n int64) [][3]int32 {
	out := make([][3]int32, count)
	for i := range out {
		u := wide(n)
		v := (u + 1 + wide(n-1)) % n
		out[i] = [3]int32{int32(u), int32(v), int32(wide(1000000000) + 1)}
	}
	return out
}

func main() {
	const count, rounds, n = 10, 5, 100000
	edges := make([][][3]int32, count)
	queries := make([][][3]int32, count)
	for c := 0; c < count; c++ {
		edges[c] = triples(n, n)
		queries[c] = triples(n, n)
	}
	var trues, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			for _, a := range distanceLimitedPathsExist(n, edges[c], queries[c]) {
				v := int64(1)
				if a {
					trues++
					v = 2
				}
				check = (check*31 + v + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d graphs of %d nodes, edges and queries, %d rounds: %d true, checksum %d\n", count, n, rounds, trues, check)
}
