// LeetCode #2843: Count Symmetric Integers -- the bench, mirrored from
// symmetric.kara: each number written out, its halves copied out and
// their digits summed.
package main

import (
	"fmt"
	"strconv"
)

func symmetric(x int64) bool {
	digits := []byte(strconv.FormatInt(x, 10))
	n := len(digits)
	if n%2 == 1 {
		return false
	}
	half := func(part []byte) int64 {
		var s int64
		for _, d := range part {
			s += int64(d - '0')
		}
		return s
	}
	return half(append([]byte(nil), digits[:n/2]...)) == half(append([]byte(nil), digits[n/2:]...))
}

func countSymmetricIntegers(low, high int64) int64 {
	var count int64
	for x := low; x <= high; x++ {
		if symmetric(x) {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 5000, 2
	seed := int64(2843)
	type rangeT struct{ low, high int64 }
	ranges := make([]rangeT, 0, count)
	for c := 0; c < count; c++ {
		a := nextRandom(&seed)%10000 + 1
		b := nextRandom(&seed)%10000 + 1
		ranges = append(ranges, rangeT{min(a, b), max(a, b)})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, rg := range ranges {
			got := countSymmetricIntegers(rg.low, rg.high)
			total += got
			check = (check*31 + got + r) % 1000000007
		}
	}
	fmt.Printf("%d ranges, %d rounds: %d in all, checksum %d\n", count, rounds, total, check)
}
