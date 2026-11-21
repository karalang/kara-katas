// LeetCode #2416: Sum of Prefix Scores of Strings -- the bench, the ★ arm:
// a trie in flat arrays, node k's child by letter c at next[26 k + c] and
// count[k] the words through it.
package main

import "fmt"

var seed int64 = 2416

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func sumPrefixScores(words [][]byte) []int64 {
	next := make([]int64, 26)
	count := make([]int64, 1)
	var zero [26]int64
	for _, w := range words {
		at := int64(0)
		for _, b := range w {
			c := int64(b - 'a')
			if next[26*at+c] == 0 {
				next[26*at+c] = int64(len(count))
				count = append(count, 0)
				next = append(next, zero[:]...)
			}
			at = next[26*at+c]
			count[at]++
		}
	}
	scores := make([]int64, 0, len(words))
	for _, w := range words {
		at := int64(0)
		score := int64(0)
		for _, b := range w {
			at = next[26*at+int64(b-'a')]
			score += count[at]
		}
		scores = append(scores, score)
	}
	return scores
}

func main() {
	lists := make([][][]byte, 0, 10)
	for i := int64(0); i < 10; i++ {
		words := make([][]byte, 0, 2000)
		for w := 0; w < 2000; w++ {
			n := 1 + nextRandom()%50
			bytes := make([]byte, 0, n)
			for k := int64(0); k < n; k++ {
				bytes = append(bytes, byte('a'+nextRandom()%(2+2*i)))
			}
			words = append(words, bytes)
		}
		lists = append(lists, words)
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, words := range lists {
			for _, s := range sumPrefixScores(words) {
				check = (check*31 + s + p) % 1000000007
			}
		}
	}
	fmt.Printf("20 passes over 10 lists of 2000 words: checksum %d\n", check)
}
