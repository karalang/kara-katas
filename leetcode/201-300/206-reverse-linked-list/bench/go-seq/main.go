package main

import "fmt"

func main() {
	var n, passes, vrange int64 = 3000, 40000, 100
	val := make([]int64, n)
	nxt := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[i] = state % vrange
		nxt[i] = -1
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		hit := p % n
		val[hit] = val[hit] + 1
		for r := int64(0); r < n; r++ {
			if r+1 < n {
				nxt[r] = r + 1
			} else {
				nxt[r] = -1
			}
		}
		var prev int64 = -1
		var cur int64 = 0
		for cur != -1 {
			saved := nxt[cur]
			nxt[cur] = prev
			prev = cur
			cur = saved
		}
		head := prev
		var passSum int64 = 0
		var idx int64 = 0
		for c := head; c != -1; c = nxt[c] {
			passSum += (idx + 1) * val[c]
			idx++
		}
		sink += passSum
	}
	fmt.Println(sink)
}
