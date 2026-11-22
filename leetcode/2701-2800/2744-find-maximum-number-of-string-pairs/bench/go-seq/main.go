// LeetCode #2744: Find Maximum Number of String Pairs -- the bench
// (pairs.kara in Go): a map of the words seen.
package main

import (
	"fmt"
	"slices"
)

func reverse(w string) string {
	r := []rune(w)
	slices.Reverse(r)
	return string(r)
}

func maximumNumberOfStringPairs(words []string) int64 {
	seen := map[string]bool{}
	var pairs int64
	for _, w := range words {
		if seen[reverse(w)] {
			pairs++
		}
		seen[w] = true
	}
	return pairs
}

var seed int64 = 2744

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 20000, 10
	lists := make([][]string, 0, count)
	for c := 0; c < count; c++ {
		words := make([]string, 0, 50)
		for len(words) < 50 {
			a := byte('a' + nextRandom()%8)
			b := byte('a' + nextRandom()%8)
			w := string([]byte{a, b})
			if !slices.Contains(words, w) {
				words = append(words, w)
			}
		}
		lists = append(lists, words)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, words := range lists {
			pairs := maximumNumberOfStringPairs(words)
			sum += pairs
			check = (check*31 + pairs + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of 50 words, %d rounds: pairs sum to %d, checksum %d\n", count, rounds, sum, check)
}
