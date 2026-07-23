package main

import "fmt"

func splitMid(nxt []int64, head int64) int64 {
	slow := head
	fast := nxt[head]
	for fast != -1 {
		fast = nxt[fast]
		if fast != -1 {
			slow = nxt[slow]
			fast = nxt[fast]
		}
	}
	mid := nxt[slow]
	nxt[slow] = -1
	return mid
}

func merge(val []int64, nxt []int64, a, b int64) int64 {
	ai, bi := a, b
	var head int64 = -1
	var tail int64 = -1
	for ai != -1 && bi != -1 {
		if val[ai] <= val[bi] {
			if head == -1 {
				head = ai
			} else {
				nxt[tail] = ai
			}
			tail = ai
			ai = nxt[ai]
		} else {
			if head == -1 {
				head = bi
			} else {
				nxt[tail] = bi
			}
			tail = bi
			bi = nxt[bi]
		}
	}
	var rest int64
	if ai != -1 {
		rest = ai
	} else {
		rest = bi
	}
	if tail != -1 {
		if rest == -1 {
			nxt[tail] = -1
		} else {
			nxt[tail] = rest
		}
	}
	return head
}

func sortChain(val []int64, nxt []int64, head int64) int64 {
	if head == -1 {
		return -1
	}
	if nxt[head] == -1 {
		return head
	}
	mid := splitMid(nxt, head)
	left := sortChain(val, nxt, head)
	right := sortChain(val, nxt, mid)
	return merge(val, nxt, left, right)
}

func main() {
	var n, passes, vr int64 = 20000, 180, 100000
	val := make([]int64, n)
	nxt := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[i] = state % vr
		nxt[i] = -1
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % n
		state = (state*1103515245 + 12345) & 2147483647
		val[idx] = state % vr

		for i := int64(0); i < n-1; i++ {
			nxt[i] = i + 1
		}
		nxt[n-1] = -1

		head := sortChain(val, nxt, 0)

		cur := head
		var pos int64 = 1
		for cur != -1 {
			sink += pos * val[cur]
			pos++
			cur = nxt[cur]
		}
	}
	fmt.Println(sink)
}
