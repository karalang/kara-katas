// LeetCode #1017: Convert to Base -2 -- bench
// Mirrors ../negabase.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func baseNeg2(n int64) string {
	if n == 0 {
		return "0"
	}
	rest := n
	digits := []byte{}
	for rest != 0 {
		bit := rest & 1
		if bit == 1 {
			digits = append(digits, '1')
		} else {
			digits = append(digits, '0')
		}
		rest = (rest - bit) / -2
	}
	for i, j := 0, len(digits)-1; i < j; i, j = i+1, j-1 {
		digits[i], digits[j] = digits[j], digits[i]
	}
	return string(digits)
}

func main() {
	var most int64 = 3000000
	var digits int64
	var check int64
	for n := int64(0); n < most+1; n++ {
		form := baseNeg2(n)
		digits += int64(len(form))
		for i := 0; i < len(form); i++ {
			var d int64 = 1
			if form[i] == '1' {
				d = 2
			}
			check = (check*3 + d) % 1000000007
		}
		check = (check * 3) % 1000000007
	}
	fmt.Printf("n = 0..%d: %d digits, checksum %d\n", most, digits, check)
}
