// LeetCode 3 — sliding-window O(n) Longest Substring Without Repeating
// Characters, Go single-threaded mirror.
// Algorithmic peer of bench/sliding_window.{kara,rs,c,py}. Same input:
// the 26-character lowercase alphabet repeated 4000 times for a 104_000-char
// string. K=20 outer iterations. Stdout sink: K * 26 = 520.
//
// Idiomatic Go: `map[rune]int64` last-index map, rebuilt per call. `right`
// is a manual char counter (not the byte index `range string` yields) so it
// matches Kāra's `s.chars()` semantic of "one tick per Unicode scalar value."
package main

import (
	"fmt"
	"strings"
)

func lengthOfLongestSubstring(s string) int64 {
	lastIdx := make(map[rune]int64)
	var left, best int64
	var right int64
	for _, c := range s {
		if prev, ok := lastIdx[c]; ok && prev >= left {
			left = prev + 1
		}
		lastIdx[c] = right
		window := right - left + 1
		if window > best {
			best = window
		}
		right++
	}
	return best
}

func main() {
	data := strings.Repeat("abcdefghijklmnopqrstuvwxyz", 4000) // 104_000 chars
	var sum int64
	for k := 0; k < 20; k++ {
		sum += lengthOfLongestSubstring(data)
	}
	fmt.Println(sum)
}
