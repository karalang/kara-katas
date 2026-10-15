// Benchmark for #652: a number for every shape, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func findDuplicateSubtrees(root *TreeNode) []*TreeNode {
	ids := map[[3]int64]int64{}
	counts := []int64{}
	found := []*TreeNode{}
	var number func(node *TreeNode) int64
	number = func(node *TreeNode) int64 {
		if node == nil {
			return 0
		}
		key := [3]int64{node.val, number(node.left), number(node.right)}
		id, ok := ids[key]
		if !ok {
			counts = append(counts, 0)
			id = int64(len(counts))
			ids[key] = id
		}
		counts[id-1]++
		if counts[id-1] == 2 {
			found = append(found, node)
		}
		return id
	}
	number(root)
	return found
}

var seed int64 = 652

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(size, spread int64) *TreeNode {
	root := &TreeNode{val: nextRandom() % spread}
	for k := int64(1); k < size; k++ {
		c := &TreeNode{val: nextRandom() % spread}
		node := root
		for {
			if nextRandom()%2 == 0 {
				if node.left != nil {
					node = node.left
				} else {
					node.left = c
					break
				}
			} else {
				if node.right != nil {
					node = node.right
				} else {
					node.right = c
					break
				}
			}
		}
	}
	return root
}

func main() {
	inputs, rounds := 4, 40
	spreads := []int64{2, 3, 5, 401}
	trees := []*TreeNode{}
	for i := 0; i < inputs; i++ {
		trees = append(trees, randomTree(100000, spreads[i]))
	}
	kinds := 0
	var checksum int64
	for r := 0; r < rounds; r++ {
		found := findDuplicateSubtrees(trees[r%inputs])
		kinds += len(found)
		for _, n := range found {
			checksum = (checksum*31 + n.val + 1) % 1000000007
		}
	}
	fmt.Printf("%d trees, %d rounds: %d kinds, checksum %d\n", inputs, rounds, kinds, checksum)
}
