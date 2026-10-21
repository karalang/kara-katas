// Benchmark for #838: Push Dominoes -- the ★ arm (the stretches between pushes).
//
// Mirrors push_dominoes.kara: the walk goes from push to push, with an L
// imagined before the line and an R after it. Between two pushes the same
// way every domino falls that way; between an R and an L the two halves
// fall inward.
package main

import (
	"fmt"
	"strings"
)

func pushDominoes(dominoes string) string {
	d := []rune(dominoes)
	n := int64(len(d))
	left := int64(-1)
	leftPush := 'L'
	for right := int64(0); right < n+1; right++ {
		rightPush := 'R'
		if right < n {
			rightPush = d[right]
		}
		if rightPush == '.' {
			continue
		}
		if leftPush == rightPush {
			for i := left + 1; i < right; i++ {
				d[i] = rightPush
			}
		} else if leftPush == 'R' {
			i, j := left+1, right-1
			for i < j {
				d[i] = 'R'
				d[j] = 'L'
				i++
				j--
			}
		}
		left = right
		leftPush = rightPush
	}
	var out strings.Builder
	for _, c := range d {
		out.WriteRune(c)
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 16 lines drawn once, each of LeetCode's longest, 10^5 dominoes,
	// line g pushing each domino left with chance 1 + 4g in 200 and right
	// with the same chance. Each round settles the next line and reads 16
	// dominoes of the result.
	count := int64(16)
	rounds := int64(1300)
	n := int64(100000)
	seed := int64(838)
	lines := make([]string, 0)
	for g := int64(0); g < count; g++ {
		pushed := 1 + 4*g
		var s strings.Builder
		for i := int64(0); i < n; i++ {
			r := nextRandom(&seed) % 200
			if r < pushed {
				s.WriteByte('L')
			} else if r < 2*pushed {
				s.WriteByte('R')
			} else {
				s.WriteByte('.')
			}
		}
		lines = append(lines, s.String())
	}
	fallen := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		out := pushDominoes(lines[round%count])
		for t := int64(0); t < 16; t++ {
			b := int64(out[(round*7919+t*6151)%n])
			if b != 46 {
				fallen++
			}
			checksum = (checksum*31 + b) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d lines: %d of the dominoes read fallen, checksum %d\n", rounds, count, fallen, checksum)
}
