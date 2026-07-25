// Benchmark harness for LeetCode #332 — Hierholzer Eulerian path.
// Mirrors reconstruct_itinerary.kara algorithm-for-algorithm.
//
// NOTE: the adjacency build uses the idiomatic append(m[k], v), which is O(1)
// amortized. The Kara mirror cannot express that — m[k].push(x) is rejected by
// codegen (kara ledger B-2026-07-25-5, open) — so it does get-copy-push-insert
// at O(degree) per edge. See ../README.md § Benchmarks.
package main

import (
	"fmt"
	"sort"
)

func visit(adj map[string][]string, cursor map[string]int64, airport string, route *[]string) {
	for {
		used := cursor[airport]
		d, ok := adj[airport]
		if !ok || int(used) >= len(d) {
			break
		}
		next := d[used]
		cursor[airport] = used + 1
		visit(adj, cursor, next, route)
	}
	*route = append(*route, airport)
}

func findItinerary(froms []string, tos []string, rot int64) []string {
	e := int64(len(froms))
	adj := make(map[string][]string)
	for i := int64(0); i < e; i++ {
		idx := (i + rot) % e
		adj[froms[idx]] = append(adj[froms[idx]], tos[idx])
	}

	for _, d := range adj {
		sort.Strings(d)
	}

	cursor := make(map[string]int64)
	route := make([]string, 0, e+1)
	visit(adj, cursor, "JFK", &route)

	for i, j := 0, len(route)-1; i < j; i, j = i+1, j-1 {
		route[i], route[j] = route[j], route[i]
	}
	return route
}

const (
	M     = 40
	L     = 24
	Iters = 250
)

func main() {
	froms := make([]string, 0, M*(L+1))
	tos := make([]string, 0, M*(L+1))
	for j := int64(0); j < M; j++ {
		prev := "JFK"
		for k := int64(0); k < L; k++ {
			cur := fmt.Sprintf("A%d", j*L+k)
			froms = append(froms, prev)
			tos = append(tos, cur)
			prev = cur
		}
		froms = append(froms, prev)
		tos = append(tos, "JFK")
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		path := findItinerary(froms, tos, it)
		for i, s := range path {
			var cs int64
			for b := 0; b < len(s); b++ {
				cs += int64(s[b])
			}
			sink += int64(i+1) * cs
		}
	}
	fmt.Println(sink)
}
