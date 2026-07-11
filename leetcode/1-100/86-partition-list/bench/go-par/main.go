// LeetCode #86 — goroutine-parallel Go mirror (par lane).
// Same batch of K=170000 independent partitions as ../go-seq/main.go; the associative
// sum reduction is split across GOMAXPROCS goroutines (chunked seed range, WaitGroup
// join, merge). Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches the
// seq mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const m int64 = 200

type ListNode struct {
	val  int64
	next *ListNode
}

func partition(head *ListNode, x int64) *ListNode {
	var lessDummy, greaterDummy ListNode
	lessTail := &lessDummy
	greaterTail := &greaterDummy
	cur := head
	for cur != nil {
		nxt := cur.next
		cur.next = nil
		if cur.val < x {
			lessTail.next = cur
			lessTail = cur
		} else {
			greaterTail.next = cur
			greaterTail = cur
		}
		cur = nxt
	}
	lessTail.next = greaterDummy.next
	return lessDummy.next
}

func build(seed int64) *ListNode {
	var dummy ListNode
	tail := &dummy
	for j := int64(0); j < m; j++ {
		node := &ListNode{val: (j*7 + seed) % 100}
		tail.next = node
		tail = node
	}
	return dummy.next
}

func fold(list *ListNode, seed int64) int64 {
	a := seed
	c := list
	for c != nil {
		a = (a*131 + (c.val + 1000)) % 1000000007
		c = c.next
	}
	return a
}

func compute(seed int64) int64 {
	return fold(partition(build(seed), 50), seed)
}

func main() {
	const total int64 = 170000
	nw := int64(runtime.GOMAXPROCS(0))
	if nw < 1 {
		nw = 1
	}
	if nw > total {
		nw = total
	}
	partials := make([]int64, nw)
	chunk := total / nw
	var wg sync.WaitGroup
	for w := int64(0); w < nw; w++ {
		start := w * chunk
		end := (w + 1) * chunk
		if w == nw-1 {
			end = total
		}
		wg.Add(1)
		go func(idx, s, e int64) {
			defer wg.Done()
			var acc int64 = 0
			for i := s; i < e; i++ {
				acc += compute(i)
			}
			partials[idx] = acc
		}(w, start, end)
	}
	wg.Wait()
	var totalSum int64 = 0
	for w := int64(0); w < nw; w++ {
		totalSum += partials[w]
	}
	fmt.Println(totalSum)
}
