// LeetCode #14 — Go seq bench peer for bench/vertical.kara. Same M/N/K,
// generator, vertical scan, and sink as the Kara / Rust / C mirrors.

package main

import "fmt"

func nthLetter(n int64) byte {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	return alphabet[n%26]
}

func makeString(prefixLen, suffixID int64) string {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	out := make([]byte, 0, prefixLen+6)
	for i := int64(0); i < prefixLen; i++ {
		out = append(out, alphabet[i])
	}
	sig := nthLetter(suffixID)
	for j := 0; j < 6; j++ {
		out = append(out, sig)
	}
	return string(out)
}

func buildCase(prefixLen, count int64) []string {
	v := make([]string, 0, count)
	for s := int64(0); s < count; s++ {
		v = append(v, makeString(prefixLen, s))
	}
	return v
}

func prefixString(s string, k int64) string {
	out := make([]byte, 0, k)
	for i := int64(0); i < k; i++ {
		out = append(out, s[i])
	}
	return string(out)
}

func longestCommonPrefix(strs []string) string {
	n := int64(len(strs))
	if n == 0 {
		return ""
	}
	first := strs[0]
	firstLen := int64(len(first))
	var col int64 = 0
	for col < firstLen {
		c := first[col]
		var s int64 = 1
		stop := false
		for s < n {
			other := strs[s]
			if col >= int64(len(other)) || other[col] != c {
				stop = true
				break
			}
			s++
		}
		if stop {
			break
		}
		col++
	}
	return prefixString(first, col)
}

func main() {
	const mCases int64 = 8
	const nStrings int64 = 16
	const kIters int64 = 1_000_000
	prefixes := [8]int64{0, 2, 4, 7, 10, 13, 16, 20}

	sets := make([][]string, 0, mCases)
	for m := int64(0); m < mCases; m++ {
		sets = append(sets, buildCase(prefixes[m], nStrings))
	}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mCases
		r := longestCommonPrefix(sets[idx])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
