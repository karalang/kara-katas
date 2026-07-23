package main

import "fmt"

type Node struct {
	val  int64
	next int64
}

func reverse(nodes []Node, head int64) int64 {
	var prev int64 = -1
	cur := head
	for cur != -1 {
		nxt := nodes[cur].next
		nodes[cur].next = prev
		prev = cur
		cur = nxt
	}
	return prev
}

func isPalindrome(nodes []Node, head int64) bool {
	if head == -1 {
		return true
	}

	slow := head
	fast := head
	for nodes[fast].next != -1 && nodes[nodes[fast].next].next != -1 {
		slow = nodes[slow].next
		fast = nodes[nodes[fast].next].next
	}

	second := reverse(nodes, nodes[slow].next)
	p1 := head
	p2 := second
	for p2 != -1 {
		if nodes[p1].val != nodes[p2].val {
			return false
		}
		p1 = nodes[p1].next
		p2 = nodes[p2].next
	}
	return true
}

func main() {
	var l int64 = 50000
	var passes int64 = 1800
	half := (l + 1) / 2

	fh := make([]int64, half)
	var state int64 = 12345
	for i := int64(0); i < half; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		fh[i] = state % 1000
	}

	nodes := make([]Node, l)
	for j := int64(0); j < l; j++ {
		if j < half {
			nodes[j].val = fh[j]
		} else {
			nodes[j].val = fh[l-1-j]
		}
		if j+1 < l {
			nodes[j].next = j + 1
		} else {
			nodes[j].next = -1
		}
	}

	var head int64 = 0
	mid := l/2 - 1
	baseMid := nodes[mid].val

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		for k := int64(0); k < l; k++ {
			if k+1 < l {
				nodes[k].next = k + 1
			} else {
				nodes[k].next = -1
			}
		}
		nodes[mid].val = baseMid + (p % 2)
		if isPalindrome(nodes, head) {
			sink += 1
		}
	}
	fmt.Println(sink)
}
