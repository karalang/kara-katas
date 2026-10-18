// LeetCode #700: Search in a Binary Search Tree -- bench program, Go mirror of the loop arm.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func searchBST(root *TreeNode, val int64) *TreeNode {
	at := root
	for at != nil {
		if val == at.val {
			return at
		}
		if val < at.val {
			at = at.left
		} else {
			at = at.right
		}
	}
	return nil
}

func leaf(v int64) *TreeNode {
	return &TreeNode{val: v}
}

func insert(root *TreeNode, v int64) {
	at := root
	for {
		if v < at.val {
			if at.left != nil {
				at = at.left
			} else {
				at.left = leaf(v)
				return
			}
		} else {
			if at.right != nil {
				at = at.right
			} else {
				at.right = leaf(v)
				return
			}
		}
	}
}

func main() {
	seed := int64(700)
	const n = int64(50000)
	trees := make([]*TreeNode, 0, 10)
	values := make([]int64, n)
	for t := 0; t < 10; t++ {
		for i := int64(0); i < n; i++ {
			values[i] = 2 * i
		}
		for i := int64(1); i < n; i++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			j := (hi*32768 + lo) % (i + 1)
			values[i], values[j] = values[j], values[i]
		}
		root := leaf(values[0])
		for i := int64(1); i < n; i++ {
			insert(root, values[i])
		}
		trees = append(trees, root)
	}
	const searches = 40000
	queries := make([]int64, searches)
	for i := range queries {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		queries[i] = (hi*32768 + lo) % (2 * n)
	}
	const rounds = 5
	found := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for _, root := range trees {
			for _, q := range queries {
				if hit := searchBST(root, q); hit != nil {
					found++
					checksum = (checksum*31 + hit.val) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds of 10 trees of %d, %d searches each: %d found, checksum %d\n", rounds, n, searches, found, checksum)
}
