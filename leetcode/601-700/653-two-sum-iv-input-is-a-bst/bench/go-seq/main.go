// Benchmark for #653: in order, then two ends, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func inOrder(node *TreeNode, values *[]int64) {
	if node == nil {
		return
	}
	inOrder(node.left, values)
	*values = append(*values, node.val)
	inOrder(node.right, values)
}

func findTarget(root *TreeNode, k int64) bool {
	values := []int64{}
	inOrder(root, &values)
	if len(values) < 2 {
		return false
	}
	low, high := 0, len(values)-1
	for low < high {
		sum := values[low] + values[high]
		if sum == k {
			return true
		} else if sum < k {
			low++
		} else {
			high--
		}
	}
	return false
}

var seed int64 = 653

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	size, queries := 200000, 300
	seen := map[int64]bool{}
	var root *TreeNode
	count := 0
	for count < size {
		hi := nextRandom()
		v := (hi*32768 + nextRandom()) % 1000000
		if seen[v] {
			continue
		}
		seen[v] = true
		count++
		c := &TreeNode{val: v}
		if root == nil {
			root = c
			continue
		}
		node := root
		for {
			if v < node.val {
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
	found := 0
	var checksum int64
	for q := 0; q < queries; q++ {
		hi := nextRandom()
		k := (hi*32768 + nextRandom()) % 3000000
		hit := findTarget(root, k)
		h := int64(0)
		if hit {
			found++
			h = 1
		}
		checksum = (checksum*2 + h) % 1000000007
	}
	fmt.Printf("%d values, %d targets: %d found, checksum %d\n", size, queries, found, checksum)
}
