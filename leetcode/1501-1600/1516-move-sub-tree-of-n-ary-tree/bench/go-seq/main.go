// LeetCode #1516 bench: the ★ arm (parent walks and a splice), as move.kara.
package main

import "fmt"

type Node struct {
	val      int64
	children []*Node
}

func parentOf(node *Node, val int64) *Node {
	for _, child := range node.children {
		if child.val == val {
			return node
		}
		if found := parentOf(child, val); found != nil {
			return found
		}
	}
	return nil
}

func contains(node *Node, val int64) bool {
	if node.val == val {
		return true
	}
	for _, child := range node.children {
		if contains(child, val) {
			return true
		}
	}
	return false
}

func without(children []*Node, val int64) []*Node {
	kept := children[:0]
	for _, c := range children {
		if c.val != val {
			kept = append(kept, c)
		}
	}
	return kept
}

func moveSubTree(root, p, q *Node) *Node {
	for _, child := range q.children {
		if child.val == p.val {
			return root
		}
	}
	pParent := parentOf(root, p.val)
	if contains(p, q.val) {
		qParent := parentOf(root, q.val)
		qParent.children = without(qParent.children, q.val)
		q.children = append(q.children, p)
		if pParent == nil {
			return q
		}
		for i, c := range pParent.children {
			if c.val == p.val {
				pParent.children[i] = q
				break
			}
		}
	} else {
		pParent.children = without(pParent.children, p.val)
		q.children = append(q.children, p)
	}
	return root
}

var seed int64 = 1516

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func fold(node *Node, check *int64) {
	*check = mix(*check, node.val)
	for _, child := range node.children {
		fold(child, check)
	}
}

func main() {
	const n int64 = 100000
	nodes := make([]*Node, n)
	for v := int64(0); v < n; v++ {
		nodes[v] = &Node{val: v}
	}
	for i := int64(1); i < n; i++ {
		a := nextRandom()
		parent := (a*32768 + nextRandom()) % i
		nodes[parent].children = append(nodes[parent].children, nodes[i])
	}
	root := nodes[0]
	var check int64
	for r := 0; r < 1000; r++ {
		a := nextRandom()
		p := (a*32768 + nextRandom()) % n
		b := nextRandom()
		q := (p + 1 + (b*32768+nextRandom())%(n-1)) % n
		root = moveSubTree(root, nodes[p], nodes[q])
		check = mix(check, root.val)
	}
	fold(root, &check)
	fmt.Printf("1000 moves in a tree of 100000 nodes: checksum %d\n", check)
}
