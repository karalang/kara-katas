package main

import "fmt"

func flip(left, right []int64, root int64) int64 {
	cur := root
	var prev int64 = -1
	var prevRight int64 = -1
	for cur != -1 {
		next := left[cur]
		left[cur] = prevRight
		prevRight = right[cur]
		right[cur] = prev
		prev = cur
		cur = next
	}
	return prev
}

func main() {
	var l int64 = 50000
	n := 2 * l
	var passes int64 = 1100

	val := make([]int64, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[c] = state
	}

	left := make([]int64, n)
	right := make([]int64, n)
	for z := int64(0); z < n; z++ {
		left[z] = -1
		right[z] = -1
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		for i := int64(0); i < l; i++ {
			if i < l-1 {
				left[i] = i + 1
			} else {
				left[i] = -1
			}
			right[i] = l + i
		}
		pp := p % l
		right[pp] = l + ((p*7 + 3) % l)

		newRoot := flip(left, right, 0)

		var chk int64 = 0
		for j := int64(0); j < n; j++ {
			chk = (chk*1103515245 + val[j]*3 + left[j] + 2 + right[j] + 5) & 2147483647
		}
		chk = (chk*1103515245 + newRoot + 1) & 2147483647
		sink = (sink + chk) & 2147483647
	}
	fmt.Println(sink)
}
