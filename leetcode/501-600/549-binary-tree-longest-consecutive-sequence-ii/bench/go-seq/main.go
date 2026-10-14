// Benchmark for #549: Go mirror of the ★ arm (post-order, two lengths a
// node); see ../binary_tree_longest_consecutive_sequence_ii.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func walk(node *TreeNode, best *int64) (int64, int64) {
	var rise, fall int64 = 1, 1
	if l := node.Left; l != nil {
		r1, f1 := walk(l, best)
		if l.Val == node.Val+1 {
			rise = r1 + 1
		} else if l.Val == node.Val-1 {
			fall = f1 + 1
		}
	}
	if r := node.Right; r != nil {
		r2, f2 := walk(r, best)
		if r.Val == node.Val+1 {
			rise = max(rise, r2+1)
		} else if r.Val == node.Val-1 {
			fall = max(fall, f2+1)
		}
	}
	*best = max(*best, rise+fall-1)
	return rise, fall
}

func longestConsecutive(root *TreeNode) int64 {
	var best int64
	if root != nil {
		walk(root, &best)
	}
	return best
}

var seed int64 = 549

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 20
	firsts := make([][]*TreeNode, count)
	for g := 0; g < count; g++ {
		spread := int64(3 + g%4)
		root := &TreeNode{Val: nextRandom() % spread}
		kept := []*TreeNode{root}
		for t := 1; t < 30000; t++ {
			c := &TreeNode{Val: nextRandom() % spread}
			node := root
			for {
				if nextRandom()%2 == 0 {
					if node.Left != nil {
						node = node.Left
					} else {
						node.Left = c
						break
					}
				} else {
					if node.Right != nil {
						node = node.Right
					} else {
						node.Right = c
						break
					}
				}
			}
			if len(kept) < 16 {
				kept = append(kept, c)
			}
		}
		firsts[g] = kept
	}
	var total, checksum int64
	for round := 0; round < 60; round++ {
		for g := 0; g < count; g++ {
			d := longestConsecutive(firsts[g][(round*7+g)%16])
			total += d
			checksum = (checksum*31 + d) % 1000000007
		}
	}
	fmt.Printf("%d trees, 60 rounds each: lengths %d, checksum %d\n", count, total, checksum)
}
