package main

import "fmt"

func main() {
	var n, passes, vrange int64 = 3000, 40000, 50
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
		target := p % vrange
		for r := int64(0); r < n; r++ {
			if r+1 < n {
				nxt[r] = r + 1
			} else {
				nxt[r] = -1
			}
		}
		var head int64 = 0
		for head != -1 && val[head] == target {
			head = nxt[head]
		}
		if head != -1 {
			prev := head
			cur := nxt[head]
			for cur != -1 {
				if val[cur] == target {
					nxt[prev] = nxt[cur]
				} else {
					prev = cur
				}
				cur = nxt[cur]
			}
		}
		var passSum int64 = 0
		for c := head; c != -1; c = nxt[c] {
			passSum += val[c]
		}
		sink += passSum
	}
	fmt.Println(sink)
}
