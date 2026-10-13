// Benchmark for #521: Go mirror of the ★ arm (the whole longer word);
// see ../find_lus_length.kara.
package main

import (
	"fmt"
	"strings"
)

func findLUSLength(a, b string) int64 {
	if a == b {
		return -1
	}
	return int64(max(len(a), len(b)))
}

var seed int64 = 521

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, letters int64) string {
	var b strings.Builder
	for i := int64(0); i < n; i++ {
		b.WriteByte(byte(97 + nextRandom()%letters))
	}
	return b.String()
}

func main() {
	// 20,000 pairs of 1 to 100 letters from 1 to 3 letters made once (a
	// third equal, a third the first word with a letter added, a third
	// unrelated), then every pair answered in each of 5,000 rounds.
	firsts := make([]string, 0, 20000)
	seconds := make([]string, 0, 20000)
	for i := 0; i < 20000; i++ {
		letters := 1 + nextRandom()%3
		a := randomWord(1+nextRandom()%100, letters)
		var b string
		switch i % 3 {
		case 0:
			b = strings.Clone(a)
		case 1:
			b = a + string(rune(97+nextRandom()%letters))
		default:
			b = randomWord(1+nextRandom()%100, letters)
		}
		firsts = append(firsts, a)
		seconds = append(seconds, b)
	}
	var total, checksum int64
	for round := int64(0); round < 5000; round++ {
		for i := range firsts {
			n := findLUSLength(firsts[i], seconds[i])
			total += n
			checksum = (checksum + (round+1)*(n+2)) % 1000000007
		}
	}
	fmt.Printf("20000 pairs, 5000 rounds: total %d, checksum %d\n", total, checksum)
}
