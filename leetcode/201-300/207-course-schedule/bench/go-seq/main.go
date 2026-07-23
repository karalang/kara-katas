package main

import "fmt"

func main() {
	var n, m, passes int64 = 5000, 15000, 8000

	esrc := make([]int64, m)
	edst := make([]int64, m)
	var state int64 = 12345
	for e := int64(0); e < m; e++ {
		state = (state*1103515245 + 12345) & 2147483647
		s := state % n
		state = (state*1103515245 + 12345) & 2147483647
		d := state % n
		esrc[e] = s
		edst[e] = d
	}

	outdeg := make([]int64, n)
	baseIndeg := make([]int64, n)
	for e := int64(0); e < m; e++ {
		outdeg[esrc[e]]++
		baseIndeg[edst[e]]++
	}

	offset := make([]int64, n+1)
	var acc int64 = 0
	for c := int64(0); c < n; c++ {
		acc += outdeg[c]
		offset[c+1] = acc
	}

	adj := make([]int64, m)
	cursor := make([]int64, n)
	for c := int64(0); c < n; c++ {
		cursor[c] = offset[c]
	}
	for e := int64(0); e < m; e++ {
		sidx := cursor[esrc[e]]
		adj[sidx] = edst[e]
		cursor[esrc[e]] = sidx + 1
	}

	indeg := make([]int64, n)
	queue := make([]int64, n)

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		for c := int64(0); c < n; c++ {
			indeg[c] = baseIndeg[c]
		}
		blocked := p % n
		indeg[blocked]++

		var qt int64 = 0
		for c := int64(0); c < n; c++ {
			if indeg[c] == 0 {
				queue[qt] = c
				qt++
			}
		}

		var qh int64 = 0
		var finished int64 = 0
		for qh < qt {
			node := queue[qh]
			qh++
			finished++
			stop := offset[node+1]
			for k := offset[node]; k < stop; k++ {
				nb := adj[k]
				indeg[nb]--
				if indeg[nb] == 0 {
					queue[qt] = nb
					qt++
				}
			}
		}
		sink += finished
	}
	fmt.Println(sink)
}
