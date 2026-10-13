// Benchmark for #508: Go mirror of the ★ arm (post-order with a count
// table); see ../find_frequent_tree_sum.kara. The count table is a fresh
// map for every call.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func subtreeSum(n *TreeNode, counts map[int64]int64) int64 {
	if n == nil {
		return 0
	}
	sum := n.val + subtreeSum(n.left, counts) + subtreeSum(n.right, counts)
	counts[sum]++
	return sum
}

func findFrequentTreeSum(root *TreeNode) []int64 {
	counts := map[int64]int64{}
	subtreeSum(root, counts)
	var best int64
	for _, c := range counts {
		if c > best {
			best = c
		}
	}
	var sums []int64
	for s, c := range counts {
		if c == best {
			sums = append(sums, s)
		}
	}
	return sums
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func build(values []int64, lo, hi int64, seed *int64) *TreeNode {
	if lo >= hi {
		return nil
	}
	mid := lo + nextRandom(seed)%(hi-lo)
	left := build(values, lo, mid, seed)
	right := build(values, mid+1, hi, seed)
	return &TreeNode{val: values[mid], left: left, right: right}
}

func main() {
	// 100 random trees of 10,000 nodes, the values from -2 to 2, from -50
	// to 50, or from the whole range -100,000 to 100,000 in turn, built
	// once. Then each is solved 30 times.
	trees := int64(100)
	seed := int64(508)
	all := make([]*TreeNode, 0, trees)
	values := make([]int64, 10000)
	for t := int64(0); t < trees; t++ {
		half := int64(100000)
		if t%3 == 0 {
			half = 2
		} else if t%3 == 1 {
			half = 50
		}
		for k := range values {
			values[k] = nextRandom(&seed)%(2*half+1) - half
		}
		all = append(all, build(values, 0, 10000, &seed))
	}
	var found, total int64
	for r := 0; r < 30; r++ {
		for t := int64(0); t < trees; t++ {
			for _, s := range findFrequentTreeSum(all[t]) {
				found++
				total += s
			}
		}
	}
	fmt.Printf("%d trees of 10000 nodes, 30 times each: %d most frequent sums, adding up to %d\n", trees, found, total)
}
