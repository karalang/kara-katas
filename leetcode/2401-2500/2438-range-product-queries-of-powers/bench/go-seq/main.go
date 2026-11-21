// LeetCode #2438: Range Product Queries of Powers -- the bench, the ★ arm:
// the exponents' prefix sums, and two to each range's sum by squaring
// modulo 10^9 + 7.
package main

import (
	"fmt"
	"math/bits"
)

const mod = 1000000007

func powerOfTwo(exponent int64) int64 {
	result, base, e := int64(1), int64(2), exponent
	for e > 0 {
		if e%2 == 1 {
			result = result * base % mod
		}
		base = base * base % mod
		e /= 2
	}
	return result
}

func productQueries(n int64, queries [][]int64) []int64 {
	prefix := []int64{0}
	for bit := int64(0); bit < 31; bit++ {
		if (n>>bit)&1 == 1 {
			prefix = append(prefix, prefix[len(prefix)-1]+bit)
		}
	}
	var answers []int64
	for _, q := range queries {
		answers = append(answers, powerOfTwo(prefix[q[1]+1]-prefix[q[0]]))
	}
	return answers
}

var seed int64 = 2438

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var values []int64
	var all [][][]int64
	for c := 0; c < 100; c++ {
		r := nextRandom()
		n := 1 + (r*32768+nextRandom())%1000000000
		k := int64(bits.OnesCount64(uint64(n)))
		var queries [][]int64
		for i := 0; i < 10000; i++ {
			a := nextRandom() % k
			b := nextRandom() % k
			queries = append(queries, []int64{min(a, b), max(a, b)})
		}
		values = append(values, n)
		all = append(all, queries)
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for c := range values {
			answers := productQueries(values[c], all[c])
			m := int64(len(answers))
			for i := int64(0); i < m; i++ {
				check = (check*31 + answers[(i+p)%m] + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 100 values of 10^4 queries: checksum %d\n", check)
}
