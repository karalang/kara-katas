package main

import "fmt"

func countDigitOne(n int64) int64 {
	if n < 0 {
		return 0
	}
	var count int64 = 0
	var pos int64 = 1
	for pos <= n {
		high := n / (pos * 10)
		cur := (n / pos) % 10
		low := n % pos
		if cur == 0 {
			count += high * pos
		} else if cur == 1 {
			count += high*pos + low + 1
		} else {
			count += (high + 1) * pos
		}
		pos *= 10
	}
	return count
}

func main() {
	var limit int64 = 6000000
	var sink int64 = 0
	for i := int64(0); i < limit; i++ {
		sink += countDigitOne(i)
	}
	fmt.Println(sink)
}
