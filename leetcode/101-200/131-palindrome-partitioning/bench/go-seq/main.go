// Benchmark harness for LeetCode #131 — Palindrome Partitioning.
// Mirrors palindrome_partitioning.kara algorithm-for-algorithm.
//
// substring ranges over the string and filters, matching the kata's O(n)
// implementation rather than using Go's O(1) s[lo:hi+1] slice — the per-piece
// cost is part of what the benchmark measures.
package main

import (
	"fmt"
	"strings"
)

func modulus() int64 { return 1000000007 }

func isPal(bytes []byte, lo int64, hi int64) bool {
	l := lo
	h := hi
	for l < h {
		if bytes[l] != bytes[h] {
			return false
		}
		l++
		h--
	}
	return true
}

func substring(s string, lo int64, hi int64) string {
	var out strings.Builder
	for i, ch := range s {
		i64 := int64(i)
		if i64 >= lo && i64 <= hi {
			out.WriteRune(ch)
		}
	}
	return out.String()
}

func partHash(path []string) int64 {
	m := modulus()
	var h int64
	for _, piece := range path {
		for i := 0; i < len(piece); i++ {
			h = (h*131 + (int64(piece[i]) - 96)) % m
		}
		h = (h*131 + 27) % m
	}
	return h
}

func backtrack(s string, bytes []byte, start int64, n int64, path *[]string, count *int64, digest *int64) {
	if start == n {
		m := modulus()
		*digest = (*digest + partHash(*path)) % m
		*count++
		return
	}
	for end := start; end < n; end++ {
		if isPal(bytes, start, end) {
			*path = append(*path, substring(s, start, end))
			backtrack(s, bytes, end+1, n, path, count, digest)
			*path = (*path)[:len(*path)-1]
		}
	}
}

const Iters = 150

func main() {
	cases := []string{
		"aaaaaaaaaaaaaaaa",
		"abababababababab",
		"abcdefghijklmnop",
		"aabaacaabaacaaba",
	}
	np := int64(len(cases))

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % np
		s := cases[idx]
		bytes := []byte(s)
		n := int64(len(bytes))
		path := make([]string, 0, 32)
		var count int64
		var digest int64
		backtrack(s, bytes, 0, n, &path, &count, &digest)
		sink = (sink + count*7 + digest) % 1000000007
	}
	fmt.Println(sink)
}
