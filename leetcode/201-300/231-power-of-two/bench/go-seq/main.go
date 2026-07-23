package main

import "fmt"

func isPowerOfTwo(n int64) bool {
	if n <= 0 {
		return false
	}
	return (n & (n - 1)) == 0
}

func main() {
	var n int64 = 130000000
	var mask int64 = 1023
	var state int64 = 12345
	var sink int64 = 0
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		v := state & mask
		if isPowerOfTwo(v) {
			sink++
		}
	}
	fmt.Println(sink)
}
