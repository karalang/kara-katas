package main

import "fmt"

func main() {
	var n, passes, vr int64 = 3000, 60, 100000
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

		var head int64 = -1
		for i := int64(0); i < n; i++ {
			v := val[i]
			if head == -1 {
				head = i
				nxt[i] = -1
			} else if val[head] >= v {
				nxt[i] = head
				head = i
			} else {
				prev := head
				scanning := true
				for scanning {
					np := nxt[prev]
					if np == -1 {
						scanning = false
					} else if val[np] < v {
						prev = np
					} else {
						scanning = false
					}
				}
				nxt[i] = nxt[prev]
				nxt[prev] = i
			}
		}

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
