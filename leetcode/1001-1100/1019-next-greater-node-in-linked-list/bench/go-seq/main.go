// LeetCode #1019: Next Greater Node In Linked List -- bench
// Mirrors ../next_greater.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func nextLargerNodes(head *ListNode) []int64 {
	values := []int64{}
	answer := []int64{}
	waiting := []int{}
	for cur := head; cur != nil; cur = cur.Next {
		v := cur.Val
		for len(waiting) > 0 && values[waiting[len(waiting)-1]] < v {
			answer[waiting[len(waiting)-1]] = v
			waiting = waiting[:len(waiting)-1]
		}
		waiting = append(waiting, len(values))
		values = append(values, v)
		answer = append(answer, 0)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var count int64 = 500
	var rounds int64 = 10
	var seed int64 = 1019
	lists := []*ListNode{}
	var nodes int64
	for t := int64(0); t < count; t++ {
		length := nextRandom(&seed)%10000 + 1
		values := make([]int64, 0, length)
		for i := int64(0); i < length; i++ {
			hi := nextRandom(&seed)
			values = append(values, (hi*32768+nextRandom(&seed))%1000000000+1)
		}
		nodes += length
		var head *ListNode
		for k := length - 1; k >= 0; k-- {
			head = &ListNode{Val: values[k], Next: head}
		}
		lists = append(lists, head)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, head := range lists {
			for _, a := range nextLargerNodes(head) {
				total = (total + a) % 1000000007
				check = (check*31 + a) % 1000000007
			}
		}
	}
	fmt.Printf("%d lists, %d nodes, %d rounds: answer sum %d, checksum %d\n", count, nodes, rounds, total, check)
}
