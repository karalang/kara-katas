// LeetCode 771 — Jewels and Stones: benchmark, the ★ arm in Go.
// 256 random pairs of 50 jewels and 50 stones, built once; ROUNDS rounds
// each count the next pair.
package main

import "fmt"

const ROUNDS = 1000000

func numJewelsInStones(jewels, stones string) int64 {
	kinds := make(map[rune]struct{})
	for _, c := range jewels {
		kinds[c] = struct{}{}
	}
	var count int64
	for _, c := range stones {
		if _, ok := kinds[c]; ok {
			count++
		}
	}
	return count
}

var seed int64 = 771

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomLetters(n int, kinds int64) string {
	out := make([]byte, n)
	for i := 0; i < n; i++ {
		k := nextRandom() % kinds
		var base int64 = 65
		if k%2 == 0 {
			base = 97
		}
		out[i] = byte(base + k/2)
	}
	return string(out)
}

func main() {
	jewels := make([]string, 0, 256)
	stones := make([]string, 0, 256)
	for i := 0; i < 256; i++ {
		jewels = append(jewels, randomLetters(50, 52))
		stones = append(stones, randomLetters(50, 52))
	}
	var total, check int64
	for round := 0; round < ROUNDS; round++ {
		k := round % 256
		count := numJewelsInStones(jewels[k], stones[k])
		total += count
		check = (check*31 + count) % 1000000007
	}
	fmt.Printf("%d rounds of 50 jewels and 50 stones: %d jewels in all, checksum %d\n", ROUNDS, total, check)
}
