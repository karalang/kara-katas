// LeetCode #2764: Is Array a Preorder of Some Binary Tree -- the bench
// (preorder.kara in Go): a stack of the nodes whose subtrees are still
// open, each node closing every subtree above its parent.
package main

import "fmt"

var seed int64 = 2764

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func isPreorder(nodes [][2]int64) bool {
	stack := make([]int64, 0, len(nodes))
	for _, node := range nodes {
		id, parent := node[0], node[1]
		for len(stack) > 0 && stack[len(stack)-1] != parent {
			stack = stack[:len(stack)-1]
		}
		if len(stack) == 0 && parent != -1 {
			return false
		}
		stack = append(stack, id)
	}
	return true
}

// a random binary tree of n nodes, ids spread over 0 to 100000, listed in
// a random preorder; then, half the time, two places swapped
func tree(n int64) [][2]int64 {
	shift := wide() % 100001
	ids := make([]int64, n)
	for k := range ids {
		ids[k] = (int64(k)*37 + shift) % 100001
	}
	kids := make([][]int64, n)
	for k := int64(1); k < n; k++ {
		p := wide() % k
		for len(kids[p]) == 2 {
			p = wide() % k
		}
		kids[p] = append(kids[p], k)
	}
	parent := make([]int64, n)
	for k := range parent {
		parent[k] = -1
	}
	for p := range kids {
		for _, c := range kids[p] {
			parent[c] = int64(p)
		}
	}
	order := make([]int64, 0, n)
	stack := []int64{0}
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		order = append(order, u)
		ks := append([]int64(nil), kids[u]...)
		if len(ks) == 2 && nextRandom()%2 == 1 {
			ks[0], ks[1] = ks[1], ks[0]
		}
		for j := len(ks) - 1; j >= 0; j-- {
			stack = append(stack, ks[j])
		}
	}
	nodes := make([][2]int64, n)
	for k, u := range order {
		p := int64(-1)
		if parent[u] >= 0 {
			p = ids[parent[u]]
		}
		nodes[k] = [2]int64{ids[u], p}
	}
	if nextRandom()%2 == 1 && n > 1 {
		i := wide() % n
		j := wide() % n
		nodes[i], nodes[j] = nodes[j], nodes[i]
	}
	return nodes
}

func main() {
	const count, rounds = 20, 100
	cases := make([][][2]int64, count)
	for c := range cases {
		cases[c] = tree(100000)
	}
	var good, check int64
	for r := int64(0); r < rounds; r++ {
		for c, nodes := range cases {
			if isPreorder(nodes) {
				good++
				check = (check*31 + int64(c) + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees of 100000, %d rounds: %d preorders, checksum %d\n", count, rounds, good, check)
}
