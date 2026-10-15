// Benchmark for #662: level by level, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

type item struct {
	node  *TreeNode
	place int64
}

func widthOfBinaryTree(root *TreeNode) int64 {
	var best int64
	var level []item
	if root != nil {
		level = append(level, item{root, 0})
	}
	for len(level) > 0 {
		first := level[0].place
		last := level[len(level)-1].place
		if last-first+1 > best {
			best = last - first + 1
		}
		var next []item
		for _, it := range level {
			p := (it.place - first) * 2
			if it.node.left != nil {
				next = append(next, item{it.node.left, p})
			}
			if it.node.right != nil {
				next = append(next, item{it.node.right, p + 1})
			}
		}
		level = next
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func leaf(v int64) *TreeNode {
	return &TreeNode{val: v}
}

func grownTree(count, levels int64, seed *int64) *TreeNode {
	root := leaf(nextRandom(seed)%201 - 100)
	made := int64(1)
	for made < count {
		at := root
		depth := int64(1)
		placed := false
		for !placed && depth < levels {
			if nextRandom(seed)%2 == 0 {
				if at.left != nil {
					at = at.left
				} else {
					at.left = leaf(nextRandom(seed)%201 - 100)
					placed = true
				}
			} else {
				if at.right != nil {
					at = at.right
				} else {
					at.right = leaf(nextRandom(seed)%201 - 100)
					placed = true
				}
			}
			depth++
		}
		if placed {
			made++
		}
	}
	return root
}

func main() {
	seed := int64(662)
	trees := make([]*TreeNode, 0, 8)
	for i := 0; i < 8; i++ {
		trees = append(trees, grownTree(3000, 31, &seed))
	}
	rounds := int64(20000)
	var sum int64
	for r := int64(0); r < rounds; r++ {
		w := widthOfBinaryTree(trees[r%8])
		sum = (sum*31 + w + r) % 1000000007
	}
	fmt.Printf("8 trees of 3000 nodes, %d rounds: checksum %d\n", rounds, sum)
}
