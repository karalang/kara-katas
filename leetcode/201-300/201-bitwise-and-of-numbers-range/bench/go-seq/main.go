package main

import "fmt"

func rangeAnd(left, right int64) int64 {
	lo, hi := left, right
	var shift int64 = 0
	for lo < hi {
		lo >>= 1
		hi >>= 1
		shift++
	}
	return lo << shift
}

func main() {
	var iters int64 = 20000000
	var state int64 = 12345
	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		state = (state*1103515245 + 12345) & 2147483647
		x := state
		state = (state*1103515245 + 12345) & 2147483647
		y := state
		var lo, hi int64
		if x < y {
			lo, hi = x, y
		} else {
			lo, hi = y, x
		}
		sink += rangeAnd(lo, hi)
	}
	fmt.Println(sink)
}
