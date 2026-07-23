package main

import "fmt"

// Build-once + punch Floyd cycle detection over an index-pool of K lists (see
// linked_list_cycle.kara). nxt[i] is the next global index or -1 for the end.
var nxt []int64

func hasCycle(head int64) bool {
	slow := head
	fast := head
	for {
		fast = nxt[fast]
		if fast < 0 {
			return false
		}
		fast = nxt[fast]
		if fast < 0 {
			return false
		}
		slow = nxt[slow]
		if slow == fast {
			return true
		}
	}
}

func main() {
	var kLists int64 = 1000
	var length int64 = 60
	var passes int64 = 3000
	var cycpct int64 = 50
	pool := kLists * length

	nxt = make([]int64, pool)
	target := make([]int64, 0, kLists)
	tail := make([]int64, 0, kLists)

	var state int64 = 12345

	for k := int64(0); k < kLists; k++ {
		base := k * length
		for j := int64(0); j < length-1; j++ {
			nxt[base+j] = base + j + 1
		}
		t := base + length - 1
		tail = append(tail, t)

		state = (state*1103515245 + 12345) & 2147483647
		coin := (state >> 16) % 100
		state = (state*1103515245 + 12345) & 2147483647
		tl := (state >> 16) % length
		target = append(target, base+tl)

		if coin < cycpct {
			nxt[t] = base + tl
		} else {
			nxt[t] = -1
		}
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := p % kLists
		ti := tail[idx]
		if nxt[ti] < 0 {
			nxt[ti] = target[idx]
		} else {
			nxt[ti] = -1
		}

		for kk := int64(0); kk < kLists; kk++ {
			if hasCycle(kk * length) {
				sink += kk + 1
			}
		}
	}

	fmt.Println(sink)
}
