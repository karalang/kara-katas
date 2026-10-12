// Benchmark for #404: mirror of sum_of_left_leaves.kara (recursion that
// knows which side it came from), over the same index pool.
package main

import "fmt"

type Node struct {
	val, left, right int64
}

func visit(nodes []Node, node int64, isLeft bool) int64 {
	if node == -1 {
		return 0
	}
	at := &nodes[node]
	if at.left == -1 && at.right == -1 {
		if isLeft {
			return at.val
		}
		return 0
	}
	return visit(nodes, at.left, true) + visit(nodes, at.right, false)
}

func sumOfLeftLeaves(nodes []Node) int64 {
	if len(nodes) == 0 {
		return 0
	}
	return visit(nodes, 0, false)
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	trees := 50
	var n int64 = 30000
	var rounds int64 = 50
	var seed int64 = 404
	var total, checksum int64
	for t := 0; t < trees; t++ {
		nodes := make([]Node, 0, n)
		nodes = append(nodes, Node{step(&seed)%201 - 100, -1, -1})
		for i := int64(1); i < n; i++ {
			p := step(&seed) % i
			side := 1 + step(&seed)%2
			for (side == 1 && nodes[p].left != -1) || (side == 2 && nodes[p].right != -1) {
				p = step(&seed) % i
				side = 1 + step(&seed)%2
			}
			nodes = append(nodes, Node{step(&seed)%201 - 100, -1, -1})
			if side == 1 {
				nodes[p].left = i
			} else {
				nodes[p].right = i
			}
		}
		for r := int64(0); r < rounds; r++ {
			nodes[r].val++
			s := sumOfLeftLeaves(nodes)
			total += s
			checksum = (checksum*31 + s + 10000000 + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of %d nodes, %d rounds: total %d, checksum %d\n", trees, n, rounds, total, checksum)
}
