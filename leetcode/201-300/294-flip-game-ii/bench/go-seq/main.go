// Benchmark twin for LeetCode #294 — same algorithm as flipgame2.kara.
//
// PARITY NOTE. Memoized backtracking, fresh map[string]bool per board,
// successors built one byte at a time to match Kāra's append-only String.
package main

import (
	"fmt"
	"strings"
)

const (
	boardLen = 22
	boards   = 300
)

func nextRand(s int64) int64 { return (s*1103515245 + 12345) & 2147483647 }

func nextStates(s string) []string {
	n := len(s)
	out := []string{}
	for i := 0; i+1 < n; i++ {
		if s[i] == '+' && s[i+1] == '+' {
			var b strings.Builder
			for j := 0; j < n; j++ {
				if j == i || j == i+1 {
					b.WriteByte('-')
				} else {
					b.WriteByte(s[j])
				}
			}
			out = append(out, b.String())
		}
	}
	return out
}

func canWin(s string, memo map[string]bool) bool {
	if v, ok := memo[s]; ok {
		return v
	}
	for _, t := range nextStates(s) {
		if !canWin(t, memo) {
			memo[s] = true
			return true
		}
	}
	memo[s] = false
	return false
}

func main() {
	seed := int64(20260821)
	densities := []int64{15, 50, 85}
	var wins, checksum int64

	for _, d := range densities {
		for b := 0; b < boards; b++ {
			var sb strings.Builder
			for i := 0; i < boardLen; i++ {
				seed = nextRand(seed)
				if (seed/65536)%100 < d {
					sb.WriteByte('+')
				} else {
					sb.WriteByte('-')
				}
			}
			s := sb.String()
			memo := make(map[string]bool)
			if canWin(s, memo) {
				wins++
			}
			checksum = (checksum*31 + int64(len(memo))) % 1000000007
		}
	}
	fmt.Printf("wins %d checksum %d\n", wins, checksum)
}
