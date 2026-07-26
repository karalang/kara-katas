// Benchmark harness for LeetCode #132 — Palindrome Partitioning II.
// Mirrors min_cut.kara algorithm-for-algorithm, including the nested [][]bool
// palindrome table.
package main

import (
	"fmt"
	"strings"
)

func minCut(s string) int64 {
	bytes := []byte(s)
	n := int64(len(bytes))
	if n <= 1 {
		return 0
	}

	pal := make([][]bool, 0, n)
	for i := int64(0); i < n; i++ {
		row := make([]bool, 0, n)
		for j := int64(0); j < n; j++ {
			row = append(row, i == j)
		}
		pal = append(pal, row)
	}

	for length := int64(2); length <= n; length++ {
		for lo := int64(0); lo <= n-length; lo++ {
			hi := lo + length - 1
			endsMatch := bytes[lo] == bytes[hi]
			innerOk := length == 2 || pal[lo+1][hi-1]
			if endsMatch && innerOk {
				pal[lo][hi] = true
			}
		}
	}

	cut := make([]int64, n)
	for i := int64(0); i < n; i++ {
		if pal[0][i] {
			cut[i] = 0
		} else {
			best := i
			for j := int64(1); j <= i; j++ {
				if pal[j][i] && (cut[j-1]+1) < best {
					best = cut[j-1] + 1
				}
			}
			cut[i] = best
		}
	}
	return cut[n-1]
}

func lcgStr(seed int64, n int64, alpha int64) string {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	var out strings.Builder
	x := seed
	for k := int64(0); k < n; k++ {
		x = (x*1103515245 + 12345) % 2147483648
		target := (x / 65536) % alpha
		for idx, ch := range alphabet {
			if int64(idx) == target {
				out.WriteRune(ch)
			}
		}
	}
	return out.String()
}

const (
	N     = 500
	Iters = 400
)

func main() {
	cases := []string{
		lcgStr(1, N, 2),
		lcgStr(2, N, 4),
		lcgStr(3, N, 26),
		lcgStr(4, N, 3),
	}
	np := int64(len(cases))

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % np
		sink = (sink + minCut(cases[idx])) % 1000000007
	}
	fmt.Println(sink)
}
