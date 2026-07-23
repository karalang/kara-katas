package main

import "fmt"

func main() {
	var n, passes int64 = 50000, 400

	val := make([]int64, n)
	left := make([]int64, n)
	right := make([]int64, n)

	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[i] = state >> 16
		left[i] = -1
		right[i] = -1
	}

	for i := int64(1); i < n; i++ {
		cur := int64(0)
		placed := false
		for !placed {
			if val[i] < val[cur] {
				if left[cur] < 0 {
					left[cur] = i
					placed = true
				} else {
					cur = left[cur]
				}
			} else {
				if right[cur] < 0 {
					right[cur] = i
					placed = true
				} else {
					cur = right[cur]
				}
			}
		}
	}

	stack := make([]int64, n)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := p % n
		val[idx]++

		sp := int64(0)
		stack[sp] = 0
		sp++
		var pos, acc int64 = 0, 0
		for sp > 0 {
			sp--
			node := stack[sp]
			acc += val[node] * (pos + 1)
			pos++
			r := right[node]
			l := left[node]
			if r >= 0 {
				stack[sp] = r
				sp++
			}
			if l >= 0 {
				stack[sp] = l
				sp++
			}
		}
		sink += acc
	}
	fmt.Println(sink)
}
