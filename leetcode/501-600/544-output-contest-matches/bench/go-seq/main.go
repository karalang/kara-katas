// Benchmark for #544: Go mirror of the ★ arm (rounds, in place); see
// ../find_contest_match.kara.
package main

import (
	"fmt"
	"strconv"
)

func findContestMatch(n int) string {
	teams := make([]string, n)
	for t := 1; t <= n; t++ {
		teams[t-1] = strconv.Itoa(t)
	}
	for m := n; m > 1; m /= 2 {
		for i := 0; i < m/2; i++ {
			teams[i] = "(" + teams[i] + "," + teams[m-1-i] + ")"
		}
	}
	return teams[0]
}

func main() {
	// 200 rounds over every size the problem allows, 2 to 4,096 teams;
	// the length of each answer is summed, and one byte of it, picked
	// by the round and the size, goes into the checksum.
	total := 0
	var checksum int64
	for r := 0; r < 200; r++ {
		for n := 2; n <= 4096; n *= 2 {
			s := findContestMatch(n)
			b := int64(s[(r*7919+n*13)%len(s)])
			total += len(s)
			checksum = (checksum*31 + b) % 1000000007
		}
	}
	fmt.Printf("200 rounds of 2 to 4096 teams: %d bytes, checksum %d\n", total, checksum)
}
