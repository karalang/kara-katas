// LeetCode #1291 bench: the ★ arm over 10^5 ranges built once, then 20
// passes, each moving every range's low up by the checksum so far, answering
// it, and folding the count and the numbers found into the checksum.
package main

import "fmt"

func sequentialDigits(low, high int64) []int64 {
	var found []int64
	for length := int64(2); length < 10; length++ {
		for first := int64(1); first < 11-length; first++ {
			var x int64
			for d := first; d < first+length; d++ {
				x = x*10 + d
			}
			if x >= low && x <= high {
				found = append(found, x)
			}
		}
	}
	return found
}

func main() {
	seed := int64(1291)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	wideRandom := func() int64 {
		a := nextRandom()
		return a*32768 + nextRandom()
	}
	type rng struct{ low, high int64 }
	ranges := make([]rng, 0, 100000)
	for a := 0; a < 100000; a++ {
		base := int64(10)
		for k := nextRandom() % 8; k > 0; k-- {
			base *= 10
		}
		span := int64(1)
		for k := nextRandom() % 10; k > 0; k-- {
			span *= 10
		}
		low := base + wideRandom()%(9*base)
		high := low + wideRandom()%span
		if high > 1000000000 {
			high = 1000000000
		}
		ranges = append(ranges, rng{low, high})
	}
	var check int64
	for p := int64(0); p < 20; p++ {
		for _, r := range ranges {
			moved := r.low + check%1000
			if moved > r.high {
				moved = r.high
			}
			found := sequentialDigits(moved, r.high)
			check = (check*31 + int64(len(found)) + p) % 1000000007
			for _, x := range found {
				check = (check*131 + x) % 1000000007
			}
		}
	}
	fmt.Printf("20 passes over 10^5 ranges: checksum %d\n", check)
}
