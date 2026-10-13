// Benchmark for #504 in Go: the ★ arm (the digits by repeated
// division); see ../../convert_to_base7.kara. Each digit is formatted
// with strconv.FormatInt and appended to the answer.
package main

import (
	"fmt"
	"strconv"
)

func convertToBase7(num int64) string {
	if num == 0 {
		return "0"
	}
	n := num
	if n < 0 {
		n = -n
	}
	var digits []int64
	for n > 0 {
		digits = append(digits, n%7)
		n /= 7
	}
	out := ""
	if num < 0 {
		out = "-"
	}
	for k := len(digits) - 1; k >= 0; k-- {
		out += strconv.FormatInt(digits[k], 10)
	}
	return out
}

func main() {
	// 5,000,001 numbers across the whole range, -10^7 to 10^7 in steps
	// of 4. Each string is read back as a decimal number, which the base
	// 7 digits name uniquely, and folded into a checksum.
	count := int64(5000001)
	var digits, checksum int64
	for i := int64(0); i < count; i++ {
		num := -10000000 + 4*i
		s := convertToBase7(num)
		digits += int64(len(s))
		read, _ := strconv.ParseInt(s, 10, 64)
		checksum = (checksum*31 + read%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("%d numbers: %d characters, checksum %d\n", count, digits, checksum)
}
