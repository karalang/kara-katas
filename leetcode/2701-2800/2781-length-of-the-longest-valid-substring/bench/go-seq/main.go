// LeetCode #2781: Length of the Longest Valid Substring -- the bench in
// Go: the ★ arm over 10 words of 10^5 letters from a to e, each against
// 10^5 forbidden words of 8 to 10 letters, all drawn first, then each
// answered 5 times, every answer building its own map.
package main

import "fmt"

func longestValidSubstring(word string, forbidden []string) int64 {
	banned := make(map[string]struct{})
	for _, w := range forbidden {
		banned[w] = struct{}{}
	}
	n := int64(len(word))
	var start, best int64
	for j := int64(0); j < n; j++ {
		for i := j; i >= start && i+10 > j; i-- {
			if _, ok := banned[word[i:j+1]]; ok {
				start = i + 1
				break
			}
		}
		best = max(best, j+1-start)
	}
	return best
}

var seed int64 = 2781

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, letters int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%letters)
	}
	return string(b)
}

func randomWords(count, shortest, longest, letters int64) []string {
	words := make([]string, 0, count)
	for c := int64(0); c < count; c++ {
		n := shortest + nextRandom()%(longest-shortest+1)
		words = append(words, randomWord(n, letters))
	}
	return words
}

type kase struct {
	word      string
	forbidden []string
}

func main() {
	count := 10
	rounds := 5
	cases := make([]kase, 0, count)
	for c := 0; c < count; c++ {
		word := randomWord(100000, 5)
		cases = append(cases, kase{word, randomWords(100000, 8, 10, 5)})
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, k := range cases {
			a := longestValidSubstring(k.word, k.forbidden)
			total += a
			check = (check*31 + a + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d words of 10^5, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, total, check)
}
