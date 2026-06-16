// LeetCode #23 — Go goroutine-parallel mirror (par lane, merge k sorted
// lists / divide-and-conquer). Same GC-managed pointer-linked build +
// pairwise-merge + full-traversal sink as ../go-seq/main.go; the K=100k
// outer reduction is split across NumCPU workers (per-worker partial +
// merge). Each iteration builds its own fresh lists, so the loop body is
// fully independent. Hand-tuned-parallel comparator. Sink matches the
// kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	kLists  = 8
	nValues = 128
	kIters  = 100_000
)

type ListNode struct {
	val  int64
	next *ListNode
}

func mergeTwoLists(l1, l2 *ListNode) *ListNode {
	dummy := &ListNode{}
	tail := dummy
	a, b := l1, l2
	for a != nil && b != nil {
		if a.val <= b.val {
			tail.next = a
			tail = a
			a = a.next
		} else {
			tail.next = b
			tail = b
			b = b.next
		}
	}
	if a != nil {
		tail.next = a
	} else {
		tail.next = b
	}
	return dummy.next
}

func mergeKLists(lists []*ListNode) *ListNode {
	k := len(lists)
	if k == 0 {
		return nil
	}
	for interval := 1; interval < k; interval *= 2 {
		for i := 0; i+interval < k; i += 2 * interval {
			lists[i] = mergeTwoLists(lists[i], lists[i+interval])
		}
	}
	return lists[0]
}

func buildList(start, step, count int64) *ListNode {
	if count <= 0 {
		return nil
	}
	head := &ListNode{val: start}
	tail := head
	v := start
	for i := int64(1); i < count; i++ {
		v += step
		node := &ListNode{val: v}
		tail.next = node
		tail = node
	}
	return head
}

func sumList(list *ListNode) int64 {
	var s int64
	for c := list; c != nil; c = c.next {
		s += c.val
	}
	return s
}

func main() {
	workers := runtime.NumCPU()
	if workers > kIters {
		workers = kIters
	}
	chunk := int64(kIters / workers)
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for wk := 0; wk < workers; wk++ {
		go func(wk int) {
			defer wg.Done()
			start := int64(wk) * chunk
			end := start + chunk
			if wk == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				lists := make([]*ListNode, 0, kLists)
				for j := int64(0); j < kLists; j++ {
					lists = append(lists, buildList(j, kLists, nValues))
				}
				s += sumList(mergeKLists(lists))
			}
			partials[wk] = s
		}(wk)
	}
	wg.Wait()
	var total int64
	for _, p := range partials {
		total += p
	}
	fmt.Println(total)
}
