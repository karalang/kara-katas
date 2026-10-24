// Benchmark: LeetCode #948 Bag of Tokens -- the ★ arm, sorted and played
// from both ends, on bags of 1000 tokens, LeetCode's largest. Mirrors
// bag_of_tokens_score.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"slices"
)

func bagOfTokensScore(tokens []int64, power int64) int64 {
	t := slices.Clone(tokens)
	slices.Sort(t)
	lo, hi := 0, len(t)-1
	p := power
	var score, best int64
	for lo <= hi {
		if p >= t[lo] {
			p -= t[lo]
			lo++
			score++
			best = max(best, score)
		} else if score > 0 && lo < hi {
			p += t[hi]
			hi--
			score--
		} else {
			break
		}
	}
	return best
}

var seed int64 = 948

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 500, 20, 1000
	bags := make([][]int64, 0, count)
	powers := make([]int64, 0, count)
	for c := 0; c < count; c++ {
		tokens := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			tokens = append(tokens, nextRandom()%10000)
		}
		bags = append(bags, tokens)
		powers = append(powers, nextRandom()%10000)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			b := (r + i) % count
			s := bagOfTokensScore(bags[b], powers[b])
			total += s
			check = (check*1000003 + s) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d bags of %d tokens: scores adding to %d, checksum %d\n", rounds, count, n, total, check)
}
