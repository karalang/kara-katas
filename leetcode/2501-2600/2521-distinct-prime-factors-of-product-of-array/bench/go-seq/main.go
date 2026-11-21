// LeetCode #2521: Distinct Prime Factors of Product of Array -- Go mirror
// of the benchmark (primes.kara): the same lists, passes, order and
// checksum.
package main

import "fmt"

func distinctPrimeFactors(nums []int64) int64 {
	primes := map[int64]struct{}{}
	for _, x := range nums {
		rest := x
		for d := int64(2); d*d <= rest; d++ {
			if rest%d == 0 {
				primes[d] = struct{}{}
				for rest%d == 0 {
					rest /= d
				}
			}
		}
		if rest > 1 {
			primes[rest] = struct{}{}
		}
	}
	return int64(len(primes))
}

var seed int64 = 2521

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 200)
	for t := range lists {
		lists[t] = make([]int64, 1000)
		for i := range lists[t] {
			lists[t][i] = nextRandom()%999 + 2
		}
	}
	const passes = 110
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, nums := range lists {
			n := check%1000 + 1
			part := append([]int64(nil), nums[:n]...)
			check = (check*31 + distinctPrimeFactors(part) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 200 lists of 1000 numbers: checksum %d\n", passes, check)
}
