// Benchmark workload for LeetCode #258 — Add Digits (Go mirror).
// Mirrors add_digits.kara algorithm-for-algorithm.
package main

import "fmt"

func addDigits(num int64) int64 {
	n := num
	for n >= 10 {
		var sum int64 = 0
		for n > 0 {
			sum += n % 10
			n /= 10
		}
		n = sum
	}
	return n
}

func main() {
	var iters int64 = 10000000
	var state int64 = 258258
	var sink int64 = 0
	for i := int64(0); i < iters; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		shift := uint((state / 65536) % 33)
		v := (state / 8) * (int64(1) << shift) % 9223372036854775807
		sink = (sink + addDigits(v)) % 1000000007
	}
	fmt.Println(sink)
}
