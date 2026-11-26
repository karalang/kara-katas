// LeetCode #1404 bench, Go: the same walk with a carry, workload and
// checksum as num_steps.kara.
package main

import (
	"fmt"
	"strings"
)

func numSteps(s string) int32 {
	bits := []rune(s)
	var steps, carry int32
	for i := len(bits) - 1; i >= 1; i-- {
		var bit int32
		if bits[i] == '1' {
			bit = 1
		}
		bit += carry
		if bit == 1 {
			steps += 2
			carry = 1
		} else {
			steps += 1
		}
	}
	return steps + carry
}

func main() {
	var seed int64 = 1404
	var b strings.Builder
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		if seed/65536%2 == 0 {
			b.WriteByte('0')
		} else {
			b.WriteByte('1')
		}
	}
	pool := b.String()
	var check int64
	for r := int64(0); r < 200000; r++ {
		at := (check + r*7919) % 99501
		s := "1" + pool[at:at+499]
		check = (check*131 + int64(numSteps(s))) % 1000000007
	}
	fmt.Printf("200000 numbers of 500 digits: checksum %d\n", check)
}
