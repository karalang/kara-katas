// Benchmark mirror of LeetCode #323 — same disjoint-set forest as
// bench/count_components.kara.
package main

import "fmt"

const (
	NODES   = 1000000
	PASSES  = 16
	STRIDE  = 9973
	MODULUS = 1073741789
)

type DisjointSet struct {
	parent []int64
	size   []int64
	sets   int64
}

func newDisjointSet(n int64) *DisjointSet {
	ds := &DisjointSet{parent: make([]int64, n), size: make([]int64, n), sets: n}
	for i := range ds.size {
		ds.size[i] = 1
	}
	return ds
}

func (ds *DisjointSet) reset() {
	for i := range ds.parent {
		ds.parent[i] = int64(i)
		ds.size[i] = 1
	}
	ds.sets = int64(len(ds.parent))
}

func (ds *DisjointSet) find(x int64) int64 {
	root := x
	for ds.parent[root] != root {
		root = ds.parent[root]
	}
	cur := x
	for ds.parent[cur] != root {
		next := ds.parent[cur]
		ds.parent[cur] = root
		cur = next
	}
	return root
}

func (ds *DisjointSet) merge(a, b int64) {
	ra := ds.find(a)
	rb := ds.find(b)
	if ra == rb {
		return
	}
	if ds.size[ra] < ds.size[rb] {
		ra, rb = rb, ra
	}
	ds.parent[rb] = ra
	ds.size[ra] += ds.size[rb]
	ds.sets--
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(seed *int64, bound int64) int64 {
	hi := next(seed)
	lo := next(seed)
	return (hi*32768 + lo) % bound
}

func main() {
	seed := int64(323)
	sink := int64(0)
	ds := newDisjointSet(NODES)
	for p := int64(0); p < PASSES; p++ {
		ds.reset()
		m := (1 + p%4) * NODES / 4
		for e := int64(0); e < m; e++ {
			a := draw(&seed, NODES)
			b := draw(&seed, NODES)
			ds.merge(a, b)
		}
		probe := int64(0)
		for i := int64(0); i < NODES; i += STRIDE {
			probe = (probe*31 + ds.find(i)) % MODULUS
		}
		sink = (sink*131 + ds.sets + probe) % MODULUS
	}
	fmt.Printf("sink %d components %d\n", sink, ds.sets)
}
