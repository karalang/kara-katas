package main

import "fmt"

func trailingZeroes(n int64) int64 {
	var count int64 = 0
	m := n / 5
	for m > 0 {
		count += m
		m /= 5
	}
	return count
}

func main() {
	var limit int64 = 35000000
	var sink int64 = 0
	for i := int64(0); i < limit; i++ {
		sink += trailingZeroes(i)
	}
	fmt.Println(sink)
}
