// Benchmark workload for LeetCode #109 — sorted list to BST, Go mirror (GC pointers).
// Build 8 sorted linked lists once (kept alive across reps by the GC), then K reps of the
// array-conversion sorted_list_to_bst on a data-dependent-selected list: walk into a local
// array, build a fresh balanced tree by middle-pick, fold, let the GC reclaim the tree.
package main

import "fmt"

const MOD int64 = 1000000007

type LNode struct {
	val  int64
	next *LNode
}
type TNode struct {
	val         int64
	left, right *TNode
}

func buildList(length, off int64) *LNode {
	var head *LNode
	for i := length - 1; i >= 0; i-- {
		head = &LNode{val: off + 1 + i, next: head}
	}
	return head
}
func buildFromArr(arr []int64, lo, hi int64) *TNode {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &TNode{
		val:   arr[mid],
		left:  buildFromArr(arr, lo, mid-1),
		right: buildFromArr(arr, mid+1, hi),
	}
}
func sortedListToBST(head *LNode) *TNode {
	arr := make([]int64, 0, 16)
	for c := head; c != nil; c = c.next {
		arr = append(arr, c.val)
	}
	return buildFromArr(arr, 0, int64(len(arr))-1)
}
func ser(n *TNode, acc int64) int64 {
	if n == nil {
		return (acc*131 + 1) % MOD
	}
	acc = (acc*131 + (n.val + 2)) % MOD
	acc = ser(n.left, acc)
	acc = ser(n.right, acc)
	return acc
}

func main() {
	pool := make([]*LNode, 8)
	for t := int64(0); t < 8; t++ {
		pool[t] = buildList(15, t*100)
	}
	var acc int64 = 1
	for rep := int64(0); rep < 1000000; rep++ {
		idx := acc % 8
		root := sortedListToBST(pool[idx])
		s := ser(root, 0)
		acc = (acc*131 + s) % MOD
	}
	fmt.Println(acc)
}
