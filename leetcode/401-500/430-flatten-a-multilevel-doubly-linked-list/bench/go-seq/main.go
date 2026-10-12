// Benchmark for #430: mirror of flatten.kara (recursion). Go's
// collector frees the nodes; the walk still breaks every link, as the
// Kāra program does.
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	val               int64
	prev, next, child *Node
}

func flattenLevel(head *Node) *Node {
	cur := head
	for {
		after := cur.next
		if cur.child != nil {
			c := cur.child
			childTail := flattenLevel(c)
			cur.next = c
			c.prev = cur
			cur.child = nil
			if after != nil {
				childTail.next = after
				after.prev = childTail
			} else {
				return childTail
			}
		}
		if after != nil {
			cur = after
		} else {
			return cur
		}
	}
}

func flatten(head *Node) *Node {
	if head != nil {
		flattenLevel(head)
	}
	return head
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func makeLevel(length int64, budget *int64, depth int64, nextVal *int64, seed *int64) *Node {
	var head, last *Node
	for i := int64(0); i < length; i++ {
		if *budget == 0 {
			break
		}
		*budget -= 1
		node := &Node{val: *nextVal}
		*nextVal += 1
		if depth < 6 && *budget > 0 && step(seed)%4 == 0 {
			childLength := 1 + step(seed)%8
			node.child = makeLevel(childLength, budget, depth+1, nextVal, seed)
		}
		if last != nil {
			last.next = node
			node.prev = last
		} else {
			head = node
		}
		last = node
	}
	return head
}

func main() {
	n := int64(1000)
	rounds := int64(2000)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(430)
	misplaced := int64(0)
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		budget := n
		nextVal := int64(1)
		cur := flatten(makeLevel(n, &budget, 0, &nextVal, &seed))
		expect := int64(1)
		for cur != nil {
			if cur.val != expect {
				misplaced++
			}
			expect++
			checksum = (checksum*31 + cur.val) % 1000000007
			next := cur.next
			cur.prev = nil
			cur.next = nil
			cur = next
		}
	}
	fmt.Printf("%d rounds of %d nodes: %d misplaced, checksum %d\n", rounds, n, misplaced, checksum)
}
