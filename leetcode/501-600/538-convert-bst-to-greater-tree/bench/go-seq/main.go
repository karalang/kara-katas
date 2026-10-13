// Benchmark for #538: Go mirror of the ★ arm (reverse in order,
// recursively); see ../convert_bst.kara.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func visit(n *TreeNode, total *int64) {
	if n == nil {
		return
	}
	visit(n.right, total)
	*total += n.val
	n.val = *total
	visit(n.left, total)
}

func convertBST(root *TreeNode) *TreeNode {
	var total int64
	visit(root, &total)
	return root
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// A search tree of distinct values, inserted in the order given; every
// node is also listed in nodes, in the same order.
func build(values []int64, nodes []*TreeNode) *TreeNode {
	root := &TreeNode{val: values[0]}
	nodes[0] = root
	for i := 1; i < len(values); i++ {
		v := values[i]
		node := root
		for {
			if v < node.val {
				if node.left != nil {
					node = node.left
				} else {
					node.left = &TreeNode{val: v}
					nodes[i] = node.left
					break
				}
			} else {
				if node.right != nil {
					node = node.right
				} else {
					node.right = &TreeNode{val: v}
					nodes[i] = node.right
					break
				}
			}
		}
	}
	return root
}

func main() {
	// 100 random search trees of 10,000 distinct values (the problem's
	// most) from -10,000 to 10,000, built once. Then 50 times over, each
	// tree has its values put back and is converted.
	trees := 100
	seed := int64(538)
	pool := make([]int64, 20001)
	for v := range pool {
		pool[v] = int64(v) - 10000
	}
	roots := make([]*TreeNode, trees)
	lists := make([][]*TreeNode, trees)
	originals := make([][]int64, trees)
	for t := 0; t < trees; t++ {
		for i := int64(0); i < 10000; i++ {
			high := nextRandom(&seed)
			j := i + (high*32768+nextRandom(&seed))%(20001-i)
			pool[i], pool[j] = pool[j], pool[i]
		}
		originals[t] = append([]int64(nil), pool[:10000]...)
		lists[t] = make([]*TreeNode, 10000)
		roots[t] = build(originals[t], lists[t])
	}
	var total, checksum int64
	for r := 0; r < 50; r++ {
		for t := 0; t < trees; t++ {
			for i, n := range lists[t] {
				n.val = originals[t][i]
			}
			top := convertBST(roots[t]).val
			total += top
			checksum = (checksum*31 + top + 1000000000) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10000 values, 50 times each: total %d, checksum %d\n", trees, total, checksum)
}
