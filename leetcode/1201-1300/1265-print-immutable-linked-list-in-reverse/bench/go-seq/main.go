// LeetCode #1265 bench, in Go: the ★ arm (by recursion: a node prints after
// everything after it has, every call through the ImmutableListNode
// interface) on 100 random lists of 1000 nodes built once, 300 rounds;
// everything each round prints folded into a checksum.
package main

import "fmt"

type ImmutableListNode interface {
	PrintValue()
	GetNext() ImmutableListNode
}

func printLinkedListInReverse(head ImmutableListNode) {
	if next := head.GetNext(); next != nil {
		printLinkedListInReverse(next)
	}
	head.PrintValue()
}

type Node struct {
	val     int64
	next    *Node
	printed *[]int64
}

func (n *Node) PrintValue() { *n.printed = append(*n.printed, n.val) }

func (n *Node) GetNext() ImmutableListNode {
	if n.next == nil {
		return nil
	}
	return n.next
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	printed := []int64{}
	seed := int64(1265)
	heads := make([]*Node, 100)
	for h := range heads {
		var head *Node
		for i := 0; i < 1000; i++ {
			head = &Node{nextRandom(&seed)%2001 - 1000, head, &printed}
		}
		heads[h] = head
	}
	var check int64
	for round := int64(0); round < 300; round++ {
		for _, h := range heads {
			printed = printed[:0]
			printLinkedListInReverse(h)
			check = (check + round) % 1000000007
			for _, v := range printed {
				check = (check*131 + v + 1000) % 1000000007
			}
		}
	}
	fmt.Printf("300 rounds of 100 lists of 1000 nodes: checksum %d\n", check)
}
