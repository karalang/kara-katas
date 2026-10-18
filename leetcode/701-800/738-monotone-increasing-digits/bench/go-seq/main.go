// LeetCode #738: Monotone Increasing Digits -- one drop, then nines.
// Benchmark mirror of the Kara star arm: the digits in a slice, the
// first place where a digit is larger than the next, a step back over
// equal digits before it, that digit lowered by one and every digit
// after it made a 9.
package main

import "fmt"

func monotoneIncreasingDigits(n int64) int64 {
	var digits []int64
	x := n
	for x > 0 {
		digits = append(digits, x%10)
		x /= 10
	}
	for a, b := 0, len(digits)-1; a < b; a, b = a+1, b-1 {
		digits[a], digits[b] = digits[b], digits[a]
	}
	i := 0
	for i+1 < len(digits) && digits[i] <= digits[i+1] {
		i++
	}
	if i+1 < len(digits) {
		for i > 0 && digits[i-1] == digits[i] {
			i--
		}
		digits[i]--
		for j := i + 1; j < len(digits); j++ {
			digits[j] = 9
		}
	}
	var out int64
	for _, d := range digits {
		out = out*10 + d
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(738)
	var total, kept int64
	for k := 0; k < 3000000; k++ {
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		n := (a*32768 + b) % 1000000001
		m := monotoneIncreasingDigits(n)
		if m == n {
			kept++
		}
		total += m
	}
	fmt.Printf("3000000 random numbers: %d already monotone, answers sum to %d\n", kept, total)
}
