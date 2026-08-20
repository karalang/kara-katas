// Benchmark twin for LeetCode #293 — same algorithm as flipgame.kara.
//
// Parity note: Kara's String is append-only, so it builds each result character
// by character with a branch per position and allocates a fresh owned string
// per result. This mirror does the same rather than make+copy, which measures a
// different algorithm.
package main

import (
	"fmt"
	"strings"
)

const length, boards = 64, 40000

func nextRand(s int64) int64 { return (s*1103515245 + 12345) & 2147483647 }

func main() {
	seed := int64(20260820)
	densities := []int64{15, 50, 85}
	var totalStates, checksum int64
	cs := make([]byte, length)

	for _, d := range densities {
		for b := 0; b < boards; b++ {
			for i := 0; i < length; i++ {
				seed = nextRand(seed)
				if (seed/65536)%100 < d {
					cs[i] = '+'
				} else {
					cs[i] = '-'
				}
			}
			out := make([]string, 0, length)
			for i := 0; i+1 < length; i++ {
				if cs[i] == '+' && cs[i+1] == '+' {
					var sb strings.Builder
					sb.Grow(length)
					for j := 0; j < length; j++ {
						if j == i || j == i+1 {
							sb.WriteByte('-')
						} else {
							sb.WriteByte(cs[j])
						}
					}
					out = append(out, sb.String())
				}
			}
			totalStates += int64(len(out))
			for _, s := range out {
				checksum = (checksum*31 + int64(len(s))) % 1000000007
			}
		}
	}
	fmt.Printf("states %d checksum %d\n", totalStates, checksum)
}
