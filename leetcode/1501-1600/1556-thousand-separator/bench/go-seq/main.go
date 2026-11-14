// LeetCode #1556: Thousand Separator -- bench: the ★ arm (a dot before
// every digit whose distance from the end is a positive multiple of three)
// over 1000000 numbers below 2^31, each with its own count of 1 to 10
// digits, drawn once, each asked 3 times. Go mirror of separator.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func thousandSeparator(n int64) string {
	digits := strconv.FormatInt(n, 10)
	length := len(digits)
	var out strings.Builder
	for i, c := range digits {
		if i > 0 && (length-i)%3 == 0 {
			out.WriteByte('.')
		}
		out.WriteRune(c)
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1556)
	numbers := make([]int64, 0, 1000000)
	for i := 0; i < 1000000; i++ {
		digits := nextRandom(&seed)%10 + 1
		top := int64(1)
		for d := int64(0); d < digits; d++ {
			top *= 10
		}
		wide := (nextRandom(&seed)*32768+nextRandom(&seed))*32768 + nextRandom(&seed)
		numbers = append(numbers, min(wide%top, 2147483647))
	}
	check, length := int64(0), 0
	for pass := 0; pass < 3; pass++ {
		for _, n := range numbers {
			text := thousandSeparator(n)
			length += len(text)
			for i := 0; i < len(text); i++ {
				check = (check*31 + int64(text[i]) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("3 passes over 1000000 numbers: %d characters, checksum %d\n", length, check)
}
