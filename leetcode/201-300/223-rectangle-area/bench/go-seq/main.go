package main

import "fmt"

func minI64(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func maxI64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func clamp0(x int64) int64 {
	if x > 0 {
		return x
	}
	return 0
}

func computeArea(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2 int64) int64 {
	areaA := (ax2 - ax1) * (ay2 - ay1)
	areaB := (bx2 - bx1) * (by2 - by1)
	overlapW := clamp0(minI64(ax2, bx2) - maxI64(ax1, bx1))
	overlapH := clamp0(minI64(ay2, by2) - maxI64(ay1, by1))
	overlap := overlapW * overlapH
	return areaA + areaB - overlap
}

func main() {
	var pairs int64 = 20000000
	var mask int64 = 16383
	var modulus int64 = 1000000007
	var state int64 = 12345
	var sink int64 = 0
	for p := int64(0); p < pairs; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		ax1 := state & mask
		state = (state*1103515245 + 12345) & 2147483647
		ax2 := ax1 + (state & mask)
		state = (state*1103515245 + 12345) & 2147483647
		ay1 := state & mask
		state = (state*1103515245 + 12345) & 2147483647
		ay2 := ay1 + (state & mask)
		state = (state*1103515245 + 12345) & 2147483647
		bx1 := state & mask
		state = (state*1103515245 + 12345) & 2147483647
		bx2 := bx1 + (state & mask)
		state = (state*1103515245 + 12345) & 2147483647
		by1 := state & mask
		state = (state*1103515245 + 12345) & 2147483647
		by2 := by1 + (state & mask)
		area := computeArea(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)
		sink = (sink + area) % modulus
	}
	fmt.Println(sink)
}
