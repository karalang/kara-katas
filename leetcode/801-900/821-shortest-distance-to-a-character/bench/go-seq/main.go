// Benchmark for #821: Shortest Distance to a Character -- the ★ arm (two sweeps).
//
// Mirrors shortest_to_char.kara: collect the characters, then a sweep
// from the left keeps the last `c` seen and a sweep from the right the
// first, and each place keeps the nearer of the two.
package main

import "fmt"

func shortestToChar(s string, c rune) []int64 {
	chars := []rune(s)
	n := int64(len(chars))
	answer := make([]int64, n)
	last := -n
	for i := int64(0); i < n; i++ {
		if chars[i] == c {
			last = i
		}
		answer[i] = i - last
	}
	last = 2 * n
	for i := n - 1; i >= 0; i-- {
		if chars[i] == c {
			last = i
		}
		if last-i < answer[i] {
			answer[i] = last - i
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 64
	rounds := 50000
	seed := int64(821)
	strings := make([]string, 0, count)
	targets := make([]rune, 0, count)
	for g := 0; g < count; g++ {
		b := make([]byte, 10000)
		for i := range b {
			b[i] = byte('a' + nextRandom(&seed)%26)
		}
		strings = append(strings, string(b))
		targets = append(targets, rune('a'+nextRandom(&seed)%26))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		answer := shortestToChar(strings[g], targets[g])
		for _, d := range answer {
			total += d
		}
		checksum = (checksum*131 + answer[round%10000]) % 1000000007
	}
	fmt.Printf("%d rounds of %d strings: total %d, checksum %d\n", rounds, count, total, checksum)
}
