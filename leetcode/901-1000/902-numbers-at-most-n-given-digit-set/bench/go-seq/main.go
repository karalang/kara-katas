// LeetCode #902: Numbers At Most N Given Digit Set -- bench program, Go.
//
// Lengths, then the digits of n from the left, asked about every one of
// the 511 sets of the digits 1 to 9, built once, in turn, each time with a
// random n from 1 to 10^9, and the counts folded into a checksum.
package main

import (
	"fmt"
	"strconv"
)

func atMostNGivenDigitSet(digits []string, n int64) int64 {
	s := strconv.FormatInt(n, 10)
	k := len(s)
	d := int64(len(digits))
	var count int64
	var power int64 = 1
	for j := 1; j < k; j++ {
		power *= d
		count += power
	}
	for i := 0; i < k; i++ {
		rest := k - i - 1
		var ways int64 = 1
		for j := 0; j < rest; j++ {
			ways *= d
		}
		var smaller int64
		equal := false
		for _, digit := range digits {
			c := digit[0]
			if c < s[i] {
				smaller++
			} else if c == s[i] {
				equal = true
			}
		}
		count += smaller * ways
		if !equal {
			return count
		}
	}
	return count + 1
}

var seed int64 = 902

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var queries int64 = 8000000
	sets := make([][]string, 0, 511)
	for mask := 1; mask < 512; mask++ {
		digits := []string{}
		for c := 1; c < 10; c++ {
			if (mask>>(c-1))&1 == 1 {
				digits = append(digits, strconv.Itoa(c))
			}
		}
		sets = append(sets, digits)
	}
	var check, total int64
	for q := int64(0); q < queries; q++ {
		hi := nextRandom()
		lo := nextRandom()
		n := 1 + (hi*32768+lo)%1000000000
		got := atMostNGivenDigitSet(sets[q%511], n)
		total += got
		check = (check*31 + got) % 1000000007
	}
	fmt.Printf("%d queries over the 511 digit sets: counts summing to %d, checksum %d\n", queries, total, check)
}
