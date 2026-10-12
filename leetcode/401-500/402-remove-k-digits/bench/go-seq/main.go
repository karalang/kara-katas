// Benchmark for #402: mirror of remove_k_digits.kara (a stack that keeps
// digits rising).
package main

import (
	"fmt"
	"strings"
)

func removeKdigits(num string, k int64) string {
	left := k
	stack := []byte{}
	for i := 0; i < len(num); i++ {
		c := num[i]
		for left > 0 && len(stack) > 0 && stack[len(stack)-1] > c {
			stack = stack[:len(stack)-1]
			left--
		}
		stack = append(stack, c)
	}
	for left > 0 {
		stack = stack[:len(stack)-1]
		left--
	}
	var out strings.Builder
	for _, c := range stack {
		if out.Len() == 0 && c == 48 {
			continue
		}
		out.WriteByte(c)
	}
	if out.Len() == 0 {
		out.WriteByte('0')
	}
	return out.String()
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	numbers := 300
	var n int64 = 100000
	var seed int64 = 402
	var kept, checksum int64
	for t := 0; t < numbers; t++ {
		var num strings.Builder
		num.WriteByte(byte(49 + step(&seed)%9))
		for i := int64(1); i < n; i++ {
			num.WriteByte(byte(48 + step(&seed)%10))
		}
		k := step(&seed) % (n + 1)
		r := removeKdigits(num.String(), k)
		kept += int64(len(r))
		for i := 0; i < len(r); i++ {
			checksum = (checksum*31 + int64(r[i])) % 1000000007
		}
	}
	fmt.Printf("%d numbers of %d digits: %d digits kept, checksum %d\n", numbers, n, kept, checksum)
}
