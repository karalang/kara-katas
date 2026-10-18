// LeetCode #742: Closest Leaf in a Binary Tree -- breadth first from k.
// Benchmark mirror of the Kara star arm: treat the tree as an undirected
// graph, each node's neighbours its children and its parent, and search
// outward from k a layer at a time; the first layer holding a leaf holds
// the nearest ones, and the smallest value of those is returned.
package main

import "fmt"

type Node struct {
	val, left, right int64
}

func findClosestLeaf(nodes []Node, k int64) int64 {
	n := len(nodes)
	var parent []int64
	start := 0
	for i := 0; i < n; i++ {
		parent = append(parent, -1)
		if nodes[i].val == k {
			start = i
		}
	}
	for i := 0; i < n; i++ {
		if nodes[i].left != -1 {
			parent[nodes[i].left] = int64(i)
		}
		if nodes[i].right != -1 {
			parent[nodes[i].right] = int64(i)
		}
	}
	var seen []bool
	for i := 0; i < n; i++ {
		seen = append(seen, false)
	}
	seen[start] = true
	layer := []int64{int64(start)}
	for {
		best := int64(-1)
		for _, x := range layer {
			node := &nodes[x]
			if node.left == -1 && node.right == -1 && (best == -1 || node.val < best) {
				best = node.val
			}
		}
		if best != -1 {
			return best
		}
		var next []int64
		for _, x := range layer {
			for _, y := range [3]int64{nodes[x].left, nodes[x].right, parent[x]} {
				if y != -1 && !seen[y] {
					seen[y] = true
					next = append(next, y)
				}
			}
		}
		layer = next
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(742)
	n := int64(1000)
	values := make([]int64, n)
	for v := int64(0); v < n; v++ {
		values[v] = v + 1
	}
	for i := int64(0); i < n; i++ {
		j := i + nextRandom(&seed)%(n-i)
		values[i], values[j] = values[j], values[i]
	}
	nodes := []Node{{values[0], -1, -1}}
	for i := int64(1); i < n; i++ {
		for {
			p := nextRandom(&seed) % i
			if nextRandom(&seed)%2 == 0 {
				if nodes[p].left == -1 {
					nodes[p].left = i
					break
				}
			} else if nodes[p].right == -1 {
				nodes[p].right = i
				break
			}
		}
		nodes = append(nodes, Node{values[i], -1, -1})
	}
	var total int64
	for r := 0; r < 60; r++ {
		a := nextRandom(&seed) % n
		b := nextRandom(&seed) % n
		nodes[a].val, nodes[b].val = nodes[b].val, nodes[a].val
		for k := int64(1); k <= n; k++ {
			total += findClosestLeaf(nodes, k)
		}
	}
	fmt.Printf("60 rounds of 1000 queries on a 1000-node tree: answers sum to %d\n", total)
}
