// LeetCode #1124: Longest Well-Performing Interval -- the bench in Go, the
// ★ arm with a `map[int64]int64` from score to first index, the same 16
// schedules and 300 rounds.
package main

import "fmt"

func longestWPI(hours []int32) int64 {
	first := make(map[int64]int64)
	var score, best int64
	for i, h := range hours {
		i := int64(i)
		if h > 8 {
			score++
		} else {
			score--
		}
		if score > 0 {
			best = i + 1
		} else {
			if j, ok := first[score-1]; ok && i-j > best {
				best = i - j
			}
			if _, ok := first[score]; !ok {
				first[score] = i
			}
		}
	}
	return best
}

var seed int64 = 1124

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	schedules := make([][]int32, 16)
	for j := range schedules {
		schedules[j] = make([]int32, 10000)
		for i := range schedules[j] {
			schedules[j][i] = int32(nextRandom() % 17)
		}
	}
	var total, check int64
	for round := int64(0); round < 300; round++ {
		for j := range schedules {
			at := (round*7919 + int64(j)*104729) % 10000
			h := schedules[j][at]
			if h > 8 {
				schedules[j][at] = h - 9
			} else {
				schedules[j][at] = 9 + h%8
			}
			answer := longestWPI(schedules[j])
			total += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 16 schedules of 10^4 days: answers total %d, checksum %d\n", total, check)
}
