// LeetCode #2472: Maximum Number of Non-overlapping Palindrome Substrings
// -- the bench, the ★ arm in Go: the greedy over starts, a palindrome of
// `k` letters from here taken first, else one of `k + 1`, each checked by
// two indices walked inward. The strings are `[]byte`.
package main

import "fmt"

func isPalindrome(c []byte, lo, hi int64) bool {
	for lo < hi {
		if c[lo] != c[hi] {
			return false
		}
		lo++
		hi--
	}
	return true
}

func maxPalindromes(c []byte, k int64) int64 {
	n := int64(len(c))
	var count, i int64
	for i+k <= n {
		if isPalindrome(c, i, i+k-1) {
			count++
			i += k
		} else if i+k < n && isPalindrome(c, i, i+k) {
			count++
			i += k + 1
		} else {
			i++
		}
	}
	return count
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2472

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 strings of 2000 letters from "ab" built once; then 2400 passes,
	// each setting one letter of every string from the checksum so far,
	// then answering it with `k` from 2 to 6 by the pass, folding the
	// count plus the pass into the checksum
	const n = 2000
	letters := []byte{'a', 'b'}
	texts := make([][]byte, 20)
	for a := range texts {
		texts[a] = make([]byte, n)
		for i := range texts[a] {
			texts[a][i] = letters[nextRandom()%2]
		}
	}
	var check int64
	for p := int64(0); p < 2400; p++ {
		k := 2 + p%5
		for a := range texts {
			texts[a][(check+int64(a))%n] = letters[check%2]
			check = (check*31 + maxPalindromes(texts[a], k) + p) % 1000000007
		}
	}
	fmt.Printf("2400 passes over 20 strings of 2000: checksum %d\n", check)
}
