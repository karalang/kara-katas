// Benchmark workload for LeetCode #138 — Copy List with Random Pointer.
//
// Pointer-graph mirror of copy_random_list.kara: N heap Node structs (a linear
// `next` chain plus one `random` edge each) are built once; the graph is
// deep-copied K times, one `random` edge repointed before each copy (the punch)
// so nothing hoists. `random` is a plain *Node (GC-managed; weak-equivalent for
// reclamation, matching Kāra's weak random). Sink = running total of a checksum
// over each copy's (val, next-id, random-id).
package main

import "fmt"

type Node struct {
	val, id      int64
	next, random *Node
}

func build(vals, rnd []int64) []*Node {
	n := int64(len(vals))
	nodes := make([]*Node, n)
	for i := int64(0); i < n; i++ {
		nodes[i] = &Node{val: vals[i], id: i}
	}
	for i := int64(0); i < n; i++ {
		if i+1 < n {
			nodes[i].next = nodes[i+1]
		}
		if rnd[i] >= 0 {
			nodes[i].random = nodes[rnd[i]]
		}
	}
	return nodes
}

func deepCopy(orig []*Node) []*Node {
	n := int64(len(orig))
	copies := make([]*Node, n)
	for i := int64(0); i < n; i++ {
		copies[i] = &Node{val: orig[i].val, id: orig[i].id}
	}
	for i := int64(0); i < n; i++ {
		if i+1 < n {
			copies[i].next = copies[i+1]
		}
		if orig[i].random != nil {
			copies[i].random = copies[orig[i].random.id]
		}
	}
	return copies
}

func checksum(copies []*Node) int64 {
	var s int64 = 0
	for _, c := range copies {
		var nextID int64 = -1
		if c.next != nil {
			nextID = c.next.id
		}
		var randID int64 = -1
		if c.random != nil {
			randID = c.random.id
		}
		s += c.val + nextID*7 + randID*13
	}
	return s
}

func main() {
	var n int64 = 3000
	var k int64 = 4000

	vals := make([]int64, n)
	rnd := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		vals[i] = (state >> 16) % 1000
		state = (state*1103515245 + 12345) & 2147483647
		r := state >> 16
		if r%4 == 0 {
			rnd[i] = -1
		} else {
			rnd[i] = r % n
		}
	}

	orig := build(vals, rnd)

	var sink int64 = 0
	for p := int64(0); p < k; p++ {
		ii := p % n
		target := (p*37 + 11) % n
		orig[ii].random = orig[target]
		copies := deepCopy(orig)
		sink += checksum(copies)
	}
	fmt.Println(sink)
}
