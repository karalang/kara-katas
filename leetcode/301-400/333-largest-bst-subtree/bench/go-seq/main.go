// Benchmark workload for LeetCode #333 — Go mirror of largest_bst.kara.
package main

import "fmt"

const (
	nodesN  = 100000
	punches = 200
	modulus = 1073741789
)

type node struct {
	val, left, right int64
}

type info struct {
	bst          bool
	size, lo, hi int64
}

func visit(nodes []node, n int64, best *int64) info {
	val := nodes[n].val
	left := nodes[n].left
	right := nodes[n].right
	bst := true
	size, lo, hi := int64(1), val, val
	if left != -1 {
		l := visit(nodes, left, best)
		if l.bst && l.hi < val {
			size += l.size
			lo = l.lo
		} else {
			bst = false
		}
	}
	if right != -1 {
		r := visit(nodes, right, best)
		if r.bst && r.lo > val {
			size += r.size
			hi = r.hi
		} else {
			bst = false
		}
	}
	if bst && size > *best {
		*best = size
	}
	return info{bst, size, lo, hi}
}

func largestBSTSubtree(nodes []node) int64 {
	if len(nodes) == 0 {
		return 0
	}
	best := int64(0)
	visit(nodes, 0, &best)
	return best
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := next(seed)
	return hi*32768 + next(seed)
}

func insert(nodes []node, v int64) []node {
	nodes = append(nodes, node{v, -1, -1})
	id := int64(len(nodes) - 1)
	cur := int64(0)
	for cur != id {
		if v < nodes[cur].val {
			if nodes[cur].left == -1 {
				nodes[cur].left = id
			}
			cur = nodes[cur].left
		} else {
			if nodes[cur].right == -1 {
				nodes[cur].right = id
			}
			cur = nodes[cur].right
		}
	}
	return nodes
}

func main() {
	seed := int64(333)
	vals := make([]int64, nodesN)
	for i := int64(0); i < nodesN; i++ {
		vals[i] = i * 2
	}
	for i := int64(0); i < nodesN; i++ {
		j := i + wide(&seed)%(nodesN-i)
		vals[i], vals[j] = vals[j], vals[i]
	}
	nodes := make([]node, 0)
	for _, v := range vals {
		nodes = insert(nodes, v)
	}
	sink := int64(0)
	for p := 0; p < punches; p++ {
		at := wide(&seed) % nodesN
		old := nodes[at].val
		nodes[at].val = wide(&seed) % (2 * nodesN)
		answer := largestBSTSubtree(nodes)
		nodes[at].val = old
		sink = (sink*1000003 + answer) % modulus
	}
	fmt.Println(sink)
}
