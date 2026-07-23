package main

import "fmt"

func listLength(next []int64, head int64) int64 {
	var n int64 = 0
	cur := head
	for cur != -1 {
		n++
		cur = next[cur]
	}
	return n
}

func advance(next []int64, head, k int64) int64 {
	cur := head
	for i := int64(0); i < k; i++ {
		cur = next[cur]
	}
	return cur
}

func intersection(next []int64, headA, headB int64) int64 {
	la := listLength(next, headA)
	lb := listLength(next, headB)
	a := headA
	b := headB
	if la > lb {
		a = advance(next, a, la-lb)
	} else {
		b = advance(next, b, lb-la)
	}
	for a != -1 && b != -1 {
		if a == b {
			return a
		}
		a = next[a]
		b = next[b]
	}
	return -1
}

func main() {
	var n int64 = 100003
	heads := n / 8
	var passes int64 = 280

	order := make([]int64, n)
	for k := int64(0); k < n; k++ {
		order[k] = (k * 48271) % n
	}

	next := make([]int64, n)
	for z := int64(0); z < n; z++ {
		next[z] = -1
	}
	for j := int64(0); j < n-1; j++ {
		next[order[j]] = order[j+1]
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		sa := p % heads
		sb := (p*131 + 7) % heads
		ha := order[sa]
		hb := order[sb]
		idx := intersection(next, ha, hb)
		sink += idx
	}
	fmt.Println(sink)
}
