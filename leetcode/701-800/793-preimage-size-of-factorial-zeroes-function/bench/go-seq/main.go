// LeetCode 793 — Preimage Size of Factorial Zeroes Function: the bench,
// in Go. Mirrors preimage_size_fzf.kara: binary search for the least x
// whose factorial has at least k zeroes at the end.
package main

import "fmt"

func zeroes(x int64) int64 {
	var count int64
	for p := x / 5; p > 0; p /= 5 {
		count += p
	}
	return count
}

func preimageSizeFZF(k int64) int64 {
	lo, hi := int64(0), 5*k+5
	for lo < hi {
		mid := lo + (hi-lo)/2
		if zeroes(mid) < k {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if zeroes(lo) == k {
		return 5
	}
	return 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(793)
	rounds := 4000000
	var fives, check int64
	for r := 0; r < rounds; r++ {
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		k := (a*32768 + b) % 1000000001
		answer := preimageSizeFZF(k)
		if answer == 5 {
			fives++
		}
		check = (check*131 + k%1000 + answer) % 1000000007
	}
	fmt.Printf("%d values of k: %d with five, checksum %d\n", rounds, fives, check)
}
