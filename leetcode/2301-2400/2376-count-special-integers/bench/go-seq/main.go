// LeetCode #2376: Count Special Integers -- the bench, the ★ arm in Go:
// the shorter numbers counted by length, then n's own length place by
// place, each place adding its smaller unused digits times the
// arrangements of the places after it.
package main

import (
	"fmt"
	"strconv"
)

func arrangements(free, places int64) int64 {
	ways := int64(1)
	for k := int64(0); k < places; k++ {
		ways *= free - k
	}
	return ways
}

func countSpecialNumbers(n int64) int64 {
	text := strconv.FormatInt(n, 10)
	digits := make([]int64, len(text))
	for i := range text {
		digits[i] = int64(text[i] - '0')
	}
	length := int64(len(digits))
	count := int64(0)
	for l := int64(1); l < length; l++ {
		count += 9 * arrangements(9, l-1)
	}
	used := make([]bool, 10)
	for i := int64(0); i < length; i++ {
		low := int64(0)
		if i == 0 {
			low = 1
		}
		for d := low; d < digits[i]; d++ {
			if !used[d] {
				count += arrangements(9-i, length-1-i)
			}
		}
		if used[digits[i]] {
			return count
		}
		used[digits[i]] = true
	}
	return count + 1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 10^5 values of 1 to 10 digits, at most 2 * 10^9
	seed := int64(2376)
	values := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		digits := 1 + nextRandom(&seed)%10
		top := int64(1)
		for k := int64(0); k < digits; k++ {
			top *= 10
		}
		high := nextRandom(&seed)
		r := high*32768 + nextRandom(&seed)
		limit := top
		if limit > 2000000001 {
			limit = 2000000001
		}
		values = append(values, 1+r%(limit-1))
	}
	check := int64(0)
	for p := int64(0); p < 100; p++ {
		for _, v := range values {
			check = (check*31 + countSpecialNumbers(v) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10^5 values: checksum %d\n", check)
}
