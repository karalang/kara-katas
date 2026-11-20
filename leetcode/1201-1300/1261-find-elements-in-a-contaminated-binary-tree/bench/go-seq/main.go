// LeetCode #1261 bench, in Go: the ★ arm (the tree recovered from the
// root down, every value kept in a hash set) on 20 random contaminated trees
// of 10000 nodes, at most 20 levels deep, built once; 120 rounds, each tree
// recovered again and asked 10000 targets, half of them nodes' places;
// the targets found counted and folded into a checksum.
package main

import (
	"fmt"
	"sort"
)

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func recover(node *TreeNode, value int64, values map[int64]bool) {
	if node != nil {
		node.Val = value
		values[value] = true
		recover(node.Left, 2*value+1, values)
		recover(node.Right, 2*value+2, values)
	}
}

type FindElements struct {
	values map[int64]bool
}

func newFindElements(root *TreeNode) FindElements {
	values := map[int64]bool{}
	recover(root, 0, values)
	return FindElements{values}
}

func (f FindElements) find(target int64) bool {
	return f.values[target]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func build(present map[int64]bool, at int64) *TreeNode {
	if !present[at] {
		return nil
	}
	return &TreeNode{-1, build(present, 2*at+1), build(present, 2*at+2)}
}

func randomPlaces(n int, seed *int64) map[int64]bool {
	places := []int64{0}
	present := map[int64]bool{0: true}
	for len(places) < n {
		p := places[nextRandom(seed)%int64(len(places))]
		child := 2*p + 1 + nextRandom(seed)%2
		if child < 2097151 && !present[child] {
			present[child] = true
			places = append(places, child)
		}
	}
	return present
}

func main() {
	seed := int64(1261)
	var trees []*TreeNode
	var targets [][]int64
	for i := 0; i < 20; i++ {
		present := randomPlaces(10000, &seed)
		places := make([]int64, 0, len(present))
		for p := range present {
			places = append(places, p)
		}
		sort.Slice(places, func(a, b int) bool { return places[a] < places[b] })
		deepest := places[len(places)-1]
		trees = append(trees, build(present, 0))
		ts := make([]int64, 10000)
		for q := range ts {
			if q%2 == 0 {
				ts[q] = places[nextRandom(&seed)%10000]
			} else {
				ts[q] = nextRandom(&seed) * 64 % (deepest + 1)
			}
		}
		targets = append(targets, ts)
	}
	found := 0
	check := int64(0)
	for r := 0; r < 120; r++ {
		for t := 0; t < 20; t++ {
			tree := newFindElements(trees[t])
			for _, target := range targets[t] {
				if tree.find(target) {
					found++
					check = (check*131 + target) % 1000000007
				}
			}
		}
	}
	fmt.Printf("120 rounds of 20 trees of 10000 nodes: %d found, checksum %d\n", found, check)
}
