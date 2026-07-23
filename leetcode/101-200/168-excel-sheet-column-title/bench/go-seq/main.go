package main

import "fmt"

func colChecksum(n int64) int64 {
	x := n
	var acc int64 = 0
	for x > 0 {
		x -= 1 // bijective base-26: shift to 0-based digit
		acc += 65 + (x % 26) // 'A' = 65
		x /= 26
	}
	return acc
}

func main() {
	var limit int64 = 50000000
	var sink int64 = 0
	for n := int64(1); n <= limit; n++ {
		sink += colChecksum(n)
	}
	fmt.Println(sink)
}
