// LeetCode #1579 bench: the same two union-find structs, in Go.
package main

import "fmt"

type dsu struct {
	parent []int64
	size   []int64
	parts  int64
}

func newDsu(n int64) *dsu {
	d := &dsu{make([]int64, n+1), make([]int64, n+1), n}
	for i := int64(0); i <= n; i++ {
		d.parent[i] = i
		d.size[i] = 1
	}
	return d
}

func (d *dsu) find(x int64) int64 {
	for d.parent[x] != x {
		d.parent[x] = d.parent[d.parent[x]]
		x = d.parent[x]
	}
	return x
}

func (d *dsu) join(a, b int64) bool {
	ra, rb := d.find(a), d.find(b)
	if ra == rb {
		return false
	}
	big, small := ra, rb
	if d.size[ra] < d.size[rb] {
		big, small = rb, ra
	}
	d.parent[small] = big
	d.size[big] += d.size[small]
	d.parts--
	return true
}

func maxNumEdgesToRemove(n int64, edges [][]int64) int64 {
	alice, bob := newDsu(n), newDsu(n)
	var kept int64
	for _, e := range edges {
		if e[0] == 3 {
			a := alice.join(e[1], e[2])
			b := bob.join(e[1], e[2])
			if a || b {
				kept++
			}
		}
	}
	for _, e := range edges {
		if e[0] == 1 && alice.join(e[1], e[2]) {
			kept++
		}
		if e[0] == 2 && bob.join(e[1], e[2]) {
			kept++
		}
	}
	if alice.parts != 1 || bob.parts != 1 {
		return -1
	}
	return int64(len(edges)) - kept
}

var seed int64 = 1579

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type graph struct {
	n     int64
	edges [][]int64
}

func main() {
	graphs := make([]graph, 0, 40)
	for g := 0; g < 40; g++ {
		n := int64(13000)
		edges := make([][]int64, 0)
		for u := int64(1); u < n; u++ {
			draws := nextRandom()%8 + 4
			for t := int64(0); t < draws; t++ {
				kind := min(nextRandom()%4, 2) + 1
				v := min(u+1+nextRandom()%12, n)
				edges = append(edges, []int64{kind, u, v})
			}
		}
		for i := int64(len(edges)) - 1; i > 0; i-- {
			j := (nextRandom()*32768 + nextRandom()) % (i + 1)
			edges[i], edges[j] = edges[j], edges[i]
		}
		graphs = append(graphs, graph{n, edges})
	}
	var check, total, stuck int64
	for _, g := range graphs {
		removed := maxNumEdgesToRemove(g.n, g.edges)
		if removed < 0 {
			stuck++
		} else {
			total += removed
		}
		check = mix(check, removed+1)
	}
	fmt.Printf("40 graphs of 13000 nodes: %d not traversable, edges removed %d, checksum %d\n", stuck, total, check)
}
