package main

import "fmt"

func reverseRange(a []int64, lo, hi int64) {
	i := lo
	j := hi
	for i < j {
		a[i], a[j] = a[j], a[i]
		i++
		j--
	}
}

func rotate(a []int64, k int64) {
	n := int64(len(a))
	if n == 0 {
		return
	}
	kk := k % n
	reverseRange(a, 0, n-1)
	reverseRange(a, 0, kk-1)
	reverseRange(a, kk, n-1)
}

func checksum(a []int64, n int64) int64 {
	var chk int64 = 0
	for i := int64(0); i < n; i++ {
		chk = ((chk * 131) + a[i]) & 2147483647
	}
	return chk
}

func main() {
	var n int64 = 30000
	var passes int64 = 4000

	a := make([]int64, n)
	var state int64 = 12345
	for b := int64(0); b < n; b++ {
		state = (state*1103515245 + 12345) & 2147483647
		a[b] = state
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		k := state % n
		rotate(a, k)
		sink += checksum(a, n)
	}
	fmt.Println(sink)
}
