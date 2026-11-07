// LeetCode #1062: Longest Repeating Substring -- the benchmark, the same
// binary search and rolling hash as lrs.kara.
package main

import (
	"bytes"
	"fmt"
)

const MOD int64 = 1000000007
const BASE int64 = 131

// Whether two starts in `s` hold the same `length` bytes.
func twice(s []byte, length int) bool {
	if length == 0 {
		return true
	}
	top := int64(1)
	for i := 1; i < length; i++ {
		top = top * BASE % MOD
	}
	hash := int64(0)
	seen := map[int64][]int{}
	for i := 0; i < len(s); i++ {
		if i >= length {
			hash = (hash - int64(s[i-length])*top%MOD + MOD) % MOD
		}
		hash = (hash*BASE + int64(s[i])) % MOD
		if i+1 >= length {
			start := i + 1 - length
			starts := seen[hash]
			for _, other := range starts {
				if bytes.Equal(s[other:other+length], s[start:start+length]) {
					return true
				}
			}
			seen[hash] = append(starts, start)
		}
	}
	return false
}

func longestRepeating(s string) int64 {
	b := []byte(s)
	// twice(lo) and not twice(hi)
	lo, hi := 0, len(b)
	for hi-lo > 1 {
		mid := lo + (hi-lo)/2
		if twice(b, mid) {
			lo = mid
		} else {
			hi = mid
		}
	}
	return int64(lo)
}

var seed int64 = 1062

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, k int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%k)
	}
	return string(b)
}

func main() {
	// 60 strings of 20000 letters over 2 to 26 of them, built once, then
	// each answered
	words := []string{}
	for w := int64(0); w < 60; w++ {
		words = append(words, randomWord(20000, 2+w%25))
	}
	var calls, total, check int64
	for _, w := range words {
		answer := longestRepeating(w)
		total += answer
		check = (check*31 + answer) % 1000000007
		calls++
	}
	fmt.Printf("%d calls: answers sum %d, checksum %d\n", calls, total, check)
}
