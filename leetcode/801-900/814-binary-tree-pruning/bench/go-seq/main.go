// Benchmark for #814: Binary Tree Pruning -- mirror of the ★ arm
// (post-order recursion), with the same workload as prune_tree.kara.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func pruneTree(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}
	root.Left = pruneTree(root.Left)
	root.Right = pruneTree(root.Right)
	if root.Val == 0 && root.Left == nil && root.Right == nil {
		return nil
	}
	return root
}

func build(vals, left, right []int64, i int64) *TreeNode {
	if i < 0 {
		return nil
	}
	l := build(vals, left, right, left[i])
	r := build(vals, left, right, right[i])
	return &TreeNode{Val: vals[i], Left: l, Right: r}
}

func weigh(root *TreeNode, depth int64) int64 {
	if root == nil {
		return 0
	}
	return (root.Val+1)*depth + weigh(root.Left, depth+1) + weigh(root.Right, depth+1)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const n int64 = 200
	const rounds int64 = 300000
	seed := int64(814)
	vals := make([][]int64, count)
	lefts := make([][]int64, count)
	rights := make([][]int64, count)
	for g := 0; g < count; g++ {
		v := make([]int64, n)
		l := make([]int64, n)
		r := make([]int64, n)
		for i := int64(0); i < n; i++ {
			if nextRandom(&seed)%8 == 0 {
				v[i] = 1
			}
			l[i] = -1
			r[i] = -1
		}
		for i := int64(1); i < n; i++ {
			for {
				p := nextRandom(&seed) % i
				if nextRandom(&seed)%2 == 0 {
					if l[p] < 0 {
						l[p] = i
						break
					}
				} else if r[p] < 0 {
					r[p] = i
					break
				}
			}
		}
		vals[g], lefts[g], rights[g] = v, l, r
	}
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % count
		i := nextRandom(&seed) % n
		vals[g][i] = 1 - vals[g][i]
		root := pruneTree(build(vals[g], lefts[g], rights[g], 0))
		checksum = (checksum*31 + weigh(root, 1)) % 1000000007
	}
	fmt.Printf("%d rounds of %d nodes: checksum %d\n", rounds, n, checksum)
}
