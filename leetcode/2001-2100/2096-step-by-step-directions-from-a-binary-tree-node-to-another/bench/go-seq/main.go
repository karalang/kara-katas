// LeetCode #2096: Step-By-Step Directions From a Binary Tree Node to
// Another -- Go mirror of the ★ arm's benchmark (directions.kara): the same
// random tree of 100000 `*TreeNode` and 1000 questions, each answered by
// the same two depth-first searches into byte slices.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wideRandom(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func wayTo(n *TreeNode, target int64, way *[]byte) bool {
	if n == nil {
		return false
	}
	if n.val == target {
		return true
	}
	*way = append(*way, 'L')
	if wayTo(n.left, target, way) {
		return true
	}
	*way = (*way)[:len(*way)-1]
	*way = append(*way, 'R')
	if wayTo(n.right, target, way) {
		return true
	}
	*way = (*way)[:len(*way)-1]
	return false
}

func getDirections(root *TreeNode, startValue, destValue int64) []byte {
	var a, b []byte
	wayTo(root, startValue, &a)
	wayTo(root, destValue, &b)
	common := 0
	for common < len(a) && common < len(b) && a[common] == b[common] {
		common++
	}
	var out []byte
	for i := common; i < len(a); i++ {
		out = append(out, 'U')
	}
	return append(out, b[common:]...)
}

func main() {
	seed := int64(2096)
	n := int64(100000)
	values := make([]int64, n)
	for i := range values {
		values[i] = int64(i) + 1
	}
	for i := n - 1; i >= 1; i-- {
		j := wideRandom(&seed) % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*TreeNode, n)
	for i, v := range values {
		nodes[i] = &TreeNode{val: v}
	}
	for k := int64(1); k < n; k++ {
		at := nodes[wideRandom(&seed)%k]
		for {
			if nextRandom(&seed)%2 == 0 {
				if at.left != nil {
					at = at.left
				} else {
					at.left = nodes[k]
					break
				}
			} else {
				if at.right != nil {
					at = at.right
				} else {
					at.right = nodes[k]
					break
				}
			}
		}
	}
	steps, check := 0, int64(0)
	for q := 0; q < 1000; q++ {
		s := wideRandom(&seed)%n + 1
		t := (s+wideRandom(&seed)%(n-1))%n + 1
		way := getDirections(nodes[0], s, t)
		steps += len(way)
		for _, c := range way {
			check = (check*31 + int64(c)) % 1000000007
		}
	}
	fmt.Printf("1000 answers: %d steps, checksum %d\n", steps, check)
}
