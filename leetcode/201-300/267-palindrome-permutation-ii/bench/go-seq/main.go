// Benchmark workload for LeetCode #267 — Palindrome Permutation II (Go mirror).
// Mirrors pal_gen.kara algorithm-for-algorithm, including the hoisted output
// buffer (see that file for why no mirror builds a string per leaf).
package main

import "fmt"

func build(counts []int64, half *[]int64, halfLen int, middle int64,
	buf []int64, acc *int64) {
	if len(*half) == halfLen {
		n := 0
		for i := 0; i < halfLen; i++ {
			buf[n] = (*half)[i]
			n++
		}
		if middle >= 0 {
			buf[n] = middle
			n++
		}
		for j := halfLen - 1; j >= 0; j-- {
			buf[n] = (*half)[j]
			n++
		}
		for k := 0; k < n; k++ {
			*acc = (*acc*31 + buf[k]) % 1000000007
		}
		return
	}
	for c := 0; c < 128; c++ {
		if counts[c] > 0 {
			counts[c]--
			*half = append(*half, int64(c))
			build(counts, half, halfLen, middle, buf, acc)
			*half = (*half)[:len(*half)-1]
			counts[c]++
		}
	}
}

func main() {
	var pairs int64 = 8
	var rounds int64 = 44

	buf := make([]int64, 64)

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		counts := make([]int64, 128)
		for p := int64(0); p < pairs; p++ {
			counts[97+p] = 2
		}
		counts[97+r%pairs]++

		var middle int64 = -1
		var halfLen int64 = 0
		for c := 0; c < 128; c++ {
			if counts[c]%2 == 1 {
				middle = int64(c)
			}
			counts[c] /= 2
			halfLen += counts[c]
		}

		var acc int64 = 0
		half := make([]int64, 0, 64)
		build(counts, &half, int(halfLen), middle, buf, &acc)
		sink = (sink*131 + acc) % 1000000007
	}
	fmt.Println(sink)
}
