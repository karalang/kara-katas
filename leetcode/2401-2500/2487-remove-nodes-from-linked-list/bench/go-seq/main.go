// LeetCode #2487: Remove Nodes From Linked List -- Go mirror of the ★ arm's
// benchmark (remove.kara): the same 22000 lists of `*ListNode`, each
// cleared by the same stack.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func removeNodes(head *ListNode) *ListNode {
	stack := []*ListNode{}
	cur := head
	for cur != nil {
		node := cur
		cur = node.Next
		for len(stack) > 0 && stack[len(stack)-1].Val < node.Val {
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, node)
	}
	var result *ListNode
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		node.Next = result
		result = node
	}
	return result
}

func build(m, round, check int64) *ListNode {
	var head *ListNode
	for j := m - 1; j >= 0; j-- {
		head = &ListNode{Val: (m-j)*10 + (round*7919+j*104729+check)%37, Next: head}
	}
	return head
}

func main() {
	rounds := int64(22000)
	kept := int64(0)
	check := int64(0)
	for r := int64(0); r < rounds; r++ {
		cur := removeNodes(build(1000, r, check))
		for cur != nil {
			kept++
			check = (check*31 + cur.Val) % 1000000007
			cur = cur.Next
		}
	}
	fmt.Printf("%d lists of 1000 nodes: %d kept, checksum %d\n", rounds, kept, check)
}
