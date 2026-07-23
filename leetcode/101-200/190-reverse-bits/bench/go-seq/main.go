package main

import "fmt"

func reverseBits(n int64) int64 {
	var result int64 = 0
	x := n
	for i := int64(0); i < 32; i++ {
		result = (result << 1) | (x & 1)
		x >>= 1
	}
	return result
}

func main() {
	var count int64 = 8000000
	var state int64 = 12345
	var sink int64 = 0
	for i := int64(0); i < count; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		sink += reverseBits(state)
	}
	fmt.Println(sink)
}
