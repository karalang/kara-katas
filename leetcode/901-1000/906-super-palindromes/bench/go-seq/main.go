// LeetCode #906: Super Palindromes -- bench program, Go.
//
// The palindromic roots built from their first halves, over random ranges
// below 10^18 given as strings. Each query counts the super-palindromes in
// its range and folds the count into a checksum.
package main

import (
	"fmt"
	"strconv"
)

func reverse(s string) string {
	b := []byte(s)
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
	return string(b)
}

func superpalindromesInRange(left, right string) int64 {
	lo, _ := strconv.ParseInt(left, 10, 64)
	hi, _ := strconv.ParseInt(right, 10, 64)
	var count int64
	for _, odd := range []bool{true, false} {
		var half int64 = 1
		for {
			digits := strconv.FormatInt(half, 10)
			back := reverse(digits)
			tail := back
			if odd {
				tail = back[1:]
			}
			root, _ := strconv.ParseInt(digits+tail, 10, 64)
			if root > hi/root {
				break
			}
			square := root * root
			shown := strconv.FormatInt(square, 10)
			if square >= lo && shown == reverse(shown) {
				count++
			}
			half++
		}
	}
	return count
}

var seed int64 = 906

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()*32768 + nextRandom()
	b := nextRandom()*32768 + nextRandom()
	return a*1073741824 + b
}

func main() {
	var queries int64 = 40
	var top int64 = 1000000000000000000
	var total, check int64
	for q := int64(0); q < queries; q++ {
		a := 1 + bigRandom()%(top-1)
		b := 1 + bigRandom()%(top-1)
		lo, hi := a, b
		if b < a {
			lo, hi = b, a
		}
		got := superpalindromesInRange(strconv.FormatInt(lo, 10), strconv.FormatInt(hi, 10))
		total += got
		check = (check*31 + got) % 1000000007
	}
	fmt.Printf("%d ranges below 10^18: counts summing to %d, checksum %d\n", queries, total, check)
}
