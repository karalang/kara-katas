// LeetCode 29 — bit-shift long division, Go seq mirror.
package main

import "fmt"

func divide(dividend int64, divisor int64) int64 {
	const intMax int64 = 2147483647
	const intMin int64 = -2147483648
	if dividend == intMin && divisor == -1 {
		return intMax
	}
	negative := (dividend < 0) != (divisor < 0)
	a := dividend
	if a < 0 {
		a = -a
	}
	b := divisor
	if b < 0 {
		b = -b
	}
	var result int64 = 0
	for a >= b {
		temp := b
		var multiple int64 = 1
		for a >= (temp << 1) {
			temp <<= 1
			multiple <<= 1
		}
		a -= temp
		result += multiple
	}
	if negative {
		return -result
	}
	return result
}

func main() {
	const N int64 = 5_000_000
	var state int64 = 1
	var sum int64 = 0
	for i := int64(0); i < N; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		dividend := state - 1073741824
		state = (state*1103515245 + 12345) % 2147483648
		divisor := (state % 2000) - 1000
		if divisor == 0 {
			divisor = 1
		}
		sum += divide(dividend, divisor)
	}
	fmt.Println(sum)
}
