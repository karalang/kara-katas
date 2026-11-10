// Benchmark: LeetCode #1100 Find K-Length Substrings With No Repeated
// Characters -- the sliding window with a count of each letter, as the
// Kāra ★ arm. Mirrors ../num_k_len_substr_no_repeats.kara.
package main

import (
	"fmt"
	"strings"
)

func numKLenSubstrNoRepeats(s string, k int64) int64 {
	b := []byte(s)
	n := int64(len(b))
	if k > 26 || k > n {
		return 0
	}
	var count [26]int64
	var repeated, found int64
	for i := int64(0); i < n; i++ {
		c := b[i] - 'a'
		count[c]++
		if count[c] == 2 {
			repeated++
		}
		if i >= k {
			out := b[i-k] - 'a'
			count[out]--
			if count[out] == 1 {
				repeated--
			}
		}
		if i >= k-1 && repeated == 0 {
			found++
		}
	}
	return found
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1100)
	texts := make([][]byte, 64)
	for j := int64(0); j < 64; j++ {
		alphabet := 8 + j%19
		t := make([]byte, 10000)
		for i := range t {
			t[i] = byte('a' + nextRandom(&seed)%alphabet)
		}
		texts[j] = t
	}
	var total, check int64
	for round := int64(0); round < 10; round++ {
		for j := int64(0); j < 64; j++ {
			at := (round*7919 + j*104729) % 10000
			texts[j][at] = byte('a' + (round+j)%26)
			s := string(texts[j])
			for q := int64(0); q < 4; q++ {
				k := (round*7+j*3+q*11)%30 + 1
				count := numKLenSubstrNoRepeats(strings.Clone(s), k)
				total += count
				check = (check*31 + count + 1) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 64 texts of 10^4 letters: %d substrings, checksum %d\n", total, check)
}
