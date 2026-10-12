// Benchmark for #437: mirror of path_sum.kara (prefix sums along the
// path) on one random tree of 100,000 nodes, queried for 200 targets.
package main

import "fmt"

type treeNode struct {
	val         int64
	left, right *treeNode
}

func countFrom(node *treeNode, prefix, target int64, seen map[int64]int64) int64 {
	if node == nil {
		return 0
	}
	sum := prefix + node.val
	found := seen[sum-target]
	seen[sum]++
	found += countFrom(node.left, sum, target, seen)
	found += countFrom(node.right, sum, target, seen)
	seen[sum]--
	return found
}

func pathSum(root *treeNode, target int64) int64 {
	seen := map[int64]int64{0: 1}
	return countFrom(root, 0, target, seen)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const size, queries = 100000, 200
	seed := int64(437)
	// Each node hangs under a random earlier node that still has a free
	// side, values in [-1000, 1000].
	root := &treeNode{val: nextRandom(&seed)%2001 - 1000}
	open := []*treeNode{root}
	for i := 1; i < size; i++ {
		at := nextRandom(&seed) % int64(len(open))
		parent := open[at]
		child := &treeNode{val: nextRandom(&seed)%2001 - 1000}
		if parent.left == nil && (parent.right != nil || nextRandom(&seed)%2 == 0) {
			parent.left = child
		} else {
			parent.right = child
		}
		if parent.left != nil && parent.right != nil {
			last := len(open) - 1
			open[at] = open[last]
			open = open[:last]
		}
		open = append(open, child)
	}
	var total, checksum int64
	for q := 0; q < queries; q++ {
		target := nextRandom(&seed)%4001 - 2000
		count := pathSum(root, target)
		total += count
		checksum = (checksum*31 + count) % 1000000007
	}
	fmt.Printf("%d targets on a tree of %d: %d paths, checksum %d\n", queries, size, total, checksum)
}
