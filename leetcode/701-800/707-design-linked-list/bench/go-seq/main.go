// LeetCode #707: Design Linked List -- singly linked, with a sentinel.
// Benchmark mirror of the Kara star arm: walk to the node before the
// position, then link a new node in after it or link past the next.
package main

import "fmt"

type Node struct {
	val  int64
	next *Node
}

type MyLinkedList struct {
	head Node
	size int64
}

func (l *MyLinkedList) before(index int64) *Node {
	at := &l.head
	for i := int64(0); i < index; i++ {
		at = at.next
	}
	return at
}

func (l *MyLinkedList) Get(index int64) int64 {
	if index < 0 || index >= l.size {
		return -1
	}
	return l.before(index).next.val
}

func (l *MyLinkedList) AddAtHead(val int64) { l.AddAtIndex(0, val) }

func (l *MyLinkedList) AddAtTail(val int64) { l.AddAtIndex(l.size, val) }

func (l *MyLinkedList) AddAtIndex(index, val int64) {
	if index < 0 || index > l.size {
		return
	}
	prev := l.before(index)
	prev.next = &Node{val: val, next: prev.next}
	l.size++
}

func (l *MyLinkedList) DeleteAtIndex(index int64) {
	if index < 0 || index >= l.size {
		return
	}
	prev := l.before(index)
	prev.next = prev.next.next
	l.size--
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(707)
	values := int64(0)
	checksum := int64(0)
	for round := 0; round < 5; round++ {
		for listNo := 0; listNo < 10; listNo++ {
			list := &MyLinkedList{}
			for i := 0; i < 6000; i++ {
				op := nextRandom(&seed) % 5
				index := nextRandom(&seed) % (list.size + 3)
				val := nextRandom(&seed) % 1001
				switch op {
				case 0:
					checksum = (checksum*31 + list.Get(index) + 2) % 1000000007
				case 1:
					list.AddAtHead(val)
				case 2:
					list.AddAtTail(val)
				case 3:
					list.AddAtIndex(index, val)
				default:
					list.DeleteAtIndex(index)
				}
			}
			values += list.size
		}
	}
	fmt.Printf("5 rounds of 10 lists of 6000 calls: %d values left, checksum %d\n", values, checksum)
}
