// Benchmark: LeetCode #988 Smallest String Starting From Leaf -- the ★
// arm, a walk carrying the path, on random trees of 8500 nodes,
// LeetCode's largest. Mirrors smallest_from_leaf.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func walk(t *TreeNode, path *[]byte, best *string, found *bool) {
	*path = append(*path, byte(97+t.Val))
	if t.Left == nil && t.Right == nil {
		p := *path
		b := make([]byte, len(p))
		for i := range p {
			b[i] = p[len(p)-1-i]
		}
		s := string(b)
		if !*found || s < *best {
			*best = s
			*found = true
		}
	} else {
		if t.Left != nil {
			walk(t.Left, path, best, found)
		}
		if t.Right != nil {
			walk(t.Right, path, best, found)
		}
	}
	*path = (*path)[:len(*path)-1]
}

func smallestFromLeaf(root *TreeNode) string {
	var path []byte
	var best string
	found := false
	walk(root, &path, &best, &found)
	return best
}

var seed int64 = 988

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	root := &TreeNode{Val: nextRandom() % 4}
	for i := 1; i < n; i++ {
		node := &TreeNode{Val: nextRandom() % 4}
		cur := root
		for {
			if nextRandom()%2 == 0 {
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

func main() {
	rounds := 100
	trees := make([]*TreeNode, 20)
	for i := range trees {
		trees[i] = randomTree(8500)
	}
	var letters, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			s := smallestFromLeaf(trees[(r+i)%20])
			letters += int64(len(s))
			for j := 0; j < len(s); j++ {
				check = (check*31 + int64(s[j])) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 20 trees of 8500 nodes: %d letters, checksum %d\n", rounds, letters, check)
}
