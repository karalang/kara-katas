// Benchmark for #450: mirror of delete_node.kara (recursive, successor's
// value copied in) on one random search tree of 1,000,000 values, built
// once, then 1,000,000 deletes of random keys.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func deleteNode(root *TreeNode, key int64) *TreeNode {
	node := root
	if node == nil {
		return nil
	}
	if key < node.val {
		node.left = deleteNode(node.left, key)
		return node
	}
	if key > node.val {
		node.right = deleteNode(node.right, key)
		return node
	}
	if node.left == nil {
		return node.right
	}
	if node.right == nil {
		return node.left
	}
	successor := node.right
	for successor.left != nil {
		successor = successor.left
	}
	node.val = successor.val
	node.right = deleteNode(node.right, successor.val)
	return node
}

func insert(root *TreeNode, v int64) *TreeNode {
	fresh := &TreeNode{val: v}
	if root == nil {
		return fresh
	}
	node := root
	for {
		if v < node.val {
			if node.left == nil {
				node.left = fresh
				break
			}
			node = node.left
		} else {
			if node.right == nil {
				node.right = fresh
				break
			}
			node = node.right
		}
	}
	return root
}

func walk(node *TreeNode, out *[]int64) {
	if node != nil {
		walk(node.left, out)
		*out = append(*out, node.val)
		walk(node.right, out)
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n, deletes = int64(1000000), 1000000
	seed := int64(450)
	// A shuffle of the even numbers below 2n.
	values := make([]int64, n)
	for i := int64(0); i < n; i++ {
		values[i] = i * 2
	}
	for i := int64(0); i < n; i++ {
		r := nextRandom(&seed) * 32768
		r += nextRandom(&seed)
		j := i + r%(n-i)
		values[i], values[j] = values[j], values[i]
	}
	var root *TreeNode
	for _, v := range values {
		root = insert(root, v)
	}
	for d := 0; d < deletes; d++ {
		key := nextRandom(&seed) * 32768
		key = (key + nextRandom(&seed)) % (2 * n)
		root = deleteNode(root, key)
	}
	left := []int64{}
	walk(root, &left)
	checksum := int64(0)
	for _, v := range left {
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("%d deletes from %d values: %d nodes left, checksum %d\n", deletes, n, len(left), checksum)
}
