// Benchmark for #426: mirror of tree_to_list.kara (the in-order
// recursion). Go's collector frees the nodes; the walk still breaks
// every link, as the Kāra program does.
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	val         int64
	left, right *Node
}

func link(node *Node, first, last **Node) {
	if node == nil {
		return
	}
	link(node.left, first, last)
	if *last != nil {
		(*last).right = node
		node.left = *last
	} else {
		*first = node
	}
	*last = node
	link(node.right, first, last)
}

func treeToDoublyList(root *Node) *Node {
	var first, last *Node
	link(root, &first, &last)
	if first == nil {
		return nil
	}
	first.left = last
	last.right = first
	return first
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func insert(root *Node, val int64) *Node {
	if root == nil {
		return &Node{val: val}
	}
	if val < root.val {
		root.left = insert(root.left, val)
	} else {
		root.right = insert(root.right, val)
	}
	return root
}

func main() {
	n := int64(50000)
	rounds := int64(20)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(426)
	order := make([]int64, n)
	for v := int64(0); v < n; v++ {
		order[v] = v
	}
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < n-1; i++ {
			a := step(&seed)
			b := step(&seed)
			j := i + (a*32768+b)%(n-i)
			order[i], order[j] = order[j], order[i]
		}
		var root *Node
		for _, v := range order {
			root = insert(root, v)
		}
		head := treeToDoublyList(root)
		checksum = (checksum*31 + head.left.val) % 1000000007
		cur := head
		for i := int64(0); i < n; i++ {
			checksum = (checksum*31 + cur.val) % 1000000007
			next := cur.right
			cur.left = nil
			cur.right = nil
			cur = next
		}
	}
	fmt.Printf("%d rounds on %d nodes: checksum %d\n", rounds, n, checksum)
}
