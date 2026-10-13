// Benchmark for #510: Go mirror of the ★ arm (down the right subtree, or
// up to the first larger ancestor); see ../inorder_successor.kara.
package main

import "fmt"

type Node struct {
	val                 int64
	left, right, parent *Node
}

func inorderSuccessor(node *Node) *Node {
	if node.right != nil {
		cur := node.right
		for cur.left != nil {
			cur = cur.left
		}
		return cur
	}
	for up := node.parent; up != nil; up = up.parent {
		if up.val > node.val {
			return up
		}
	}
	return nil
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// Every node of the search tree of the values, in insertion order.
func build(values []int64) []*Node {
	root := &Node{val: values[0]}
	nodes := []*Node{root}
	for _, v := range values[1:] {
		leaf := &Node{val: v}
		node := root
		for {
			slot := &node.right
			if v < node.val {
				slot = &node.left
			}
			if *slot != nil {
				node = *slot
			} else {
				leaf.parent = node
				*slot = leaf
				break
			}
		}
		nodes = append(nodes, leaf)
	}
	return nodes
}

func main() {
	// 100 random search trees of 10,000 different values, the j-th value
	// j * 20 plus less than 20, shuffled, built once. Then the successor
	// of every node, 50 times over.
	trees, size := 100, int64(10000)
	seed := int64(510)
	all := make([][]*Node, 0, trees)
	for t := 0; t < trees; t++ {
		values := make([]int64, size)
		for j := int64(0); j < size; j++ {
			values[j] = j*20 + nextRandom(&seed)%20 - 100000
		}
		for i := int64(1); i < size; i++ {
			k := nextRandom(&seed) % (i + 1)
			values[i], values[k] = values[k], values[i]
		}
		all = append(all, build(values))
	}
	var nulls, checksum int64
	for r := 0; r < 50; r++ {
		for t := 0; t < trees; t++ {
			for _, node := range all[t] {
				if s := inorderSuccessor(node); s != nil {
					checksum = (checksum + s.val + 100000) % 1000000007
				} else {
					nulls++
				}
			}
		}
	}
	fmt.Printf("%d trees of %d nodes, 50 times each: %d without a successor, checksum %d\n", trees, size, nulls, checksum)
}
