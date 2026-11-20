// LeetCode #1724: Checking Existence of Edge Length Limited Paths II --
// the bench (dist.kara): a union-find by rank, never compressed, each
// node keeping the weight of the edge that hung it under its parent; a
// query climbs from each node while the links stay below the limit.
package main

import (
	"fmt"
	"math"
	"sort"
)

type DistanceLimitedPathsExist struct {
	parent []int
	joined []int32
}

func root(parent []int, x int) int {
	for parent[x] != x {
		x = parent[x]
	}
	return x
}

func newPaths(n int, edgeList [][3]int32) *DistanceLimitedPathsExist {
	edges := append([][3]int32(nil), edgeList...)
	sort.SliceStable(edges, func(a, b int) bool { return edges[a][2] < edges[b][2] })
	parent := make([]int, n)
	joined := make([]int32, n)
	rank := make([]int, n)
	for i := range parent {
		parent[i] = i
		joined[i] = math.MaxInt32
	}
	for _, e := range edges {
		a := root(parent, int(e[0]))
		b := root(parent, int(e[1]))
		if a == b {
			continue
		}
		if rank[a] < rank[b] {
			a, b = b, a
		}
		parent[b] = a
		joined[b] = e[2]
		if rank[a] == rank[b] {
			rank[a]++
		}
	}
	return &DistanceLimitedPathsExist{parent, joined}
}

func (g *DistanceLimitedPathsExist) rootBelow(x int, limit int32) int {
	for g.joined[x] < limit {
		x = g.parent[x]
	}
	return x
}

func (g *DistanceLimitedPathsExist) query(p, q, limit int32) bool {
	return g.rootBelow(int(p), limit) == g.rootBelow(int(q), limit)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	count := 20
	var rounds int64 = 50
	var n int64 = 10000
	m := 10000
	asked := 10000
	var top int64 = 1000000000
	var seed int64 = 1724
	edgeLists := make([][][3]int32, count)
	queries := make([][][3]int32, count)
	for c := 0; c < count; c++ {
		edgeLists[c] = make([][3]int32, m)
		for i := range edgeLists[c] {
			u := wide(&seed) % n
			v := wide(&seed) % (n - 1)
			if v >= u {
				v++
			}
			edgeLists[c][i] = [3]int32{int32(u), int32(v), int32(wide(&seed)%top + 1)}
		}
		queries[c] = make([][3]int32, asked)
		for i := range queries[c] {
			p := wide(&seed) % n
			q := wide(&seed) % (n - 1)
			if q >= p {
				q++
			}
			queries[c][i] = [3]int32{int32(p), int32(q), int32(wide(&seed)%top + 1)}
		}
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			graph := newPaths(int(n), edgeLists[c])
			for _, qu := range queries[c] {
				answer := graph.query(qu[0], qu[1], qu[2])
				var bit int64 = 1
				if answer {
					yes++
					bit = 2
				}
				check = (check*31 + bit + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d graphs of %d nodes and %d edges, %d queries each, %d rounds: %d paths, checksum %d\n", count, n, m, asked, rounds, yes, check)
}
