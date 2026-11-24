// LeetCode #1290 bench: the ★ arm over 10^4 lists of 30 nodes built once,
// then 500 passes, each setting one bit of every list and reading it back.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func getDecimalValue(head *ListNode) int64 {
	var value int64
	for cur := head; cur != nil; cur = cur.Next {
		value = value*2 + cur.Val
	}
	return value
}

func setBit(head *ListNode, k, bit int64) {
	var i int64
	for cur := head; cur != nil; cur = cur.Next {
		if i == k {
			cur.Val = bit
			return
		}
		i++
	}
}

func main() {
	seed := int64(1290)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	heads := make([]*ListNode, 0, 10000)
	for a := 0; a < 10000; a++ {
		var head *ListNode
		for j := 0; j < 30; j++ {
			head = &ListNode{Val: nextRandom() % 2, Next: head}
		}
		heads = append(heads, head)
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for a := range heads {
			setBit(heads[a], (check+int64(a))%30, check/16%2)
			check = (check*31 + getDecimalValue(heads[a]) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 10^4 lists of 30 bits: checksum %d\n", check)
}
