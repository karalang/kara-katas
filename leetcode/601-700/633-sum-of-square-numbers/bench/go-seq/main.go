// LeetCode 633 -- Sum of Square Numbers, bench mirror in Go.
//
// The ★ arm of judge_square_sum.kara: two pointers from 0 and from the
// integer square root of `c`, found by binary search. Same values, same
// output line.
package main

import "fmt"

func root(n int64) int64 {
	lo, hi := int64(0), min(n, 3037000499)+1
	for hi-lo > 1 {
		mid := (lo + hi) / 2
		if mid*mid <= n {
			lo = mid
		} else {
			hi = mid
		}
	}
	return lo
}

func judgeSquareSum(c int64) bool {
	a, b := int64(0), root(c)
	for a <= b {
		sum := a*a + b*b
		if sum == c {
			return true
		}
		if sum < c {
			a++
		} else {
			b--
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(633)
	values := []int64{}
	for i := 0; i < 10000; i++ {
		wide := nextRandom(&seed) * 32768
		wide += nextRandom(&seed)
		values = append(values, wide*2+nextRandom(&seed)%2)
	}
	var yes, checksum int64
	for _, c := range values {
		if judgeSquareSum(c) {
			yes++
			checksum = (checksum*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d values: %d sums of two squares, checksum %d\n", len(values), yes, checksum)
}
