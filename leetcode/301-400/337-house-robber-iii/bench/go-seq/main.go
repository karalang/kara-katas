// Benchmark workload for LeetCode #337 — Go mirror of house_robber_iii.kara.
package main

import "fmt"

const (
	houses  = 500000
	punches = 100
	modulus = 1073741789
)

type node struct {
	val, left, right int64
}

func max64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func visit(nodes []node, n int64) (int64, int64) {
	if n == -1 {
		return 0, 0
	}
	lr, ls := visit(nodes, nodes[n].left)
	rr, rs := visit(nodes, nodes[n].right)
	return nodes[n].val + ls + rs, max64(lr, ls) + max64(rr, rs)
}

func rob(nodes []node) int64 {
	if len(nodes) == 0 {
		return 0
	}
	r, s := visit(nodes, 0)
	return max64(r, s)
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := next(seed)
	return hi*32768 + next(seed)
}

func main() {
	seed := int64(337)
	nodes := make([]node, 0, houses)
	for i := int64(0); i < houses; i++ {
		nodes = append(nodes, node{next(&seed) % 10001, -1, -1})
		if i == 0 {
			continue
		}
		cur := int64(0)
		for {
			if next(&seed)%2 == 0 {
				if nodes[cur].left == -1 {
					nodes[cur].left = i
					break
				}
				cur = nodes[cur].left
			} else {
				if nodes[cur].right == -1 {
					nodes[cur].right = i
					break
				}
				cur = nodes[cur].right
			}
		}
	}
	sink := int64(0)
	for p := 0; p < punches; p++ {
		at := wide(&seed) % houses
		old := nodes[at].val
		nodes[at].val = next(&seed) % 10001
		answer := rob(nodes)
		nodes[at].val = old
		sink = (sink*1000003 + answer) % modulus
	}
	fmt.Println(sink)
}
