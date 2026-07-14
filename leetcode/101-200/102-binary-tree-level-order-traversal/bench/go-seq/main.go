// Benchmark workload for LeetCode #102 — level order, Go mirror (GC *Node).
// Build 8 BSTs once, then K reps of DFS-with-depth level_order on a data-dependent-
// selected tree, folding the whole [][]int64 result into a rolling hash. Each rep
// allocates a fresh [][]int64 and lets the GC reclaim it.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func insert(root *Node, v int64) *Node {
	if root == nil {
		return &Node{val: v}
	}
	if v < root.val {
		root.left = insert(root.left, v)
	} else {
		root.right = insert(root.right, v)
	}
	return root
}

func dfs(node *Node, depth int, result *[][]int64) {
	if node == nil {
		return
	}
	if depth == len(*result) {
		*result = append(*result, []int64{})
	}
	(*result)[depth] = append((*result)[depth], node.val)
	dfs(node.left, depth+1, result)
	dfs(node.right, depth+1, result)
}

func levelOrder(root *Node) [][]int64 {
	var result [][]int64
	dfs(root, 0, &result)
	return result
}

func main() {
	base := []int64{16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30}
	bn := len(base)
	pool := make([]*Node, 8)
	for t := 0; t < 8; t++ {
		var root *Node
		for k := 0; k < bn; k++ {
			root = insert(root, base[(k+t)%bn])
		}
		pool[t] = root
	}
	var acc int64 = 1
	for rep := int64(0); rep < 1500000; rep++ {
		idx := acc % 8
		levels := levelOrder(pool[idx])
		acc = (acc*131 + int64(len(levels))) % MOD
		for _, lvl := range levels {
			acc = (acc*131 + int64(len(lvl))) % MOD
			for _, v := range lvl {
				acc = (acc*131 + v) % MOD
			}
		}
	}
	fmt.Println(acc)
}
