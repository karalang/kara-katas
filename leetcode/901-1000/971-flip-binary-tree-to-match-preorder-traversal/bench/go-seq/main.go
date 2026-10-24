// Benchmark: LeetCode #971 Flip Binary Tree To Match Preorder Traversal
// -- the ★ arm, one walk flipping where the voyage says, on 200 random
// trees of 100 nodes. Mirrors flip_match_voyage.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func walk(t *TreeNode, voyage []int64, i *int, flipped *[]int64) bool {
	if t == nil {
		return true
	}
	if t.Val != voyage[*i] {
		return false
	}
	*i++
	if t.Left != nil && t.Left.Val != voyage[*i] {
		*flipped = append(*flipped, t.Val)
		return walk(t.Right, voyage, i, flipped) && walk(t.Left, voyage, i, flipped)
	}
	return walk(t.Left, voyage, i, flipped) && walk(t.Right, voyage, i, flipped)
}

func flipMatchVoyage(root *TreeNode, voyage []int64) []int64 {
	i := 0
	var flipped []int64
	if walk(root, voyage, &i, &flipped) {
		return flipped
	}
	return []int64{-1}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPermutation(n int64, seed *int64) []int64 {
	a := make([]int64, n)
	for v := int64(1); v <= n; v++ {
		a[v-1] = v
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom(seed) % (i + 1)
		a[i], a[j] = a[j], a[i]
	}
	return a
}

func randomTree(vals []int64, seed *int64) *TreeNode {
	root := &TreeNode{Val: vals[0]}
	for _, v := range vals[1:] {
		node := &TreeNode{Val: v}
		cur := root
		for {
			if nextRandom(seed)%2 == 0 {
				if cur.Left != nil {
					cur = cur.Left
				} else {
					cur.Left = node
					break
				}
			} else {
				if cur.Right != nil {
					cur = cur.Right
				} else {
					cur.Right = node
					break
				}
			}
		}
	}
	return root
}

func randomVoyage(t *TreeNode, seed *int64, out *[]int64) {
	if t == nil {
		return
	}
	*out = append(*out, t.Val)
	if nextRandom(seed)%2 == 0 {
		randomVoyage(t.Left, seed, out)
		randomVoyage(t.Right, seed, out)
	} else {
		randomVoyage(t.Right, seed, out)
		randomVoyage(t.Left, seed, out)
	}
}

func main() {
	rounds, count := 1000, 200
	seed := int64(971)
	trees := make([]*TreeNode, count)
	voyages := make([][]int64, count)
	for c := 0; c < count; c++ {
		trees[c] = randomTree(randomPermutation(100, &seed), &seed)
		var voyage []int64
		randomVoyage(trees[c], &seed, &voyage)
		if c%4 == 3 {
			i := nextRandom(&seed) % 100
			j := nextRandom(&seed) % 100
			voyage[i], voyage[j] = voyage[j], voyage[i]
		}
		voyages[c] = voyage
	}
	flips, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for s := 0; s < count; s++ {
			c := (r + s) % count
			for _, v := range flipMatchVoyage(trees[c], voyages[c]) {
				flips++
				check = (check*31 + v + 2) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d trees of 100 nodes: %d values, checksum %d\n", rounds, count, flips, check)
}
