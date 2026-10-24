// Benchmark: LeetCode #940 Distinct Subsequences II -- the ★ arm,
// doubling less the repeats, on 100 words of 2000 letters, LeetCode's
// longest, in 200 rounds. Mirrors distinct_subseq_ii.kara, .c, .rs and
// .py.
package main

import "fmt"

func distinctSubseqII(s string) int64 {
	const m int64 = 1000000007
	n := len(s)
	count := make([]int64, 1, n+1)
	count[0] = 1
	var last [26]int
	for i := 0; i < n; i++ {
		c := s[i] - 'a'
		next := 2 * count[i] % m
		if last[c] > 0 {
			next = (next - count[last[c]-1] + m) % m
		}
		count = append(count, next)
		last[c] = i + 1
	}
	return (count[n] - 1 + m) % m
}

var seed int64 = 940

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 200, 100
	words := make([]string, 0, count)
	for w := 0; w < count; w++ {
		k := 1 + nextRandom()%26
		b := make([]byte, 2000)
		for i := range b {
			b[i] = byte(nextRandom()%k + 'a')
		}
		words = append(words, string(b))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			a := distinctSubseqII(words[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d words of 2000 letters: counts adding to %d, checksum %d\n", rounds, count, total, check)
}
