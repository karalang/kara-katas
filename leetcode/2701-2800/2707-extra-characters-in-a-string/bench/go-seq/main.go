// LeetCode #2707: Extra Characters in a String -- the bench (extra.kara in
// Go): the fewest extra characters of each suffix, from the end back,
// with the dictionary a map asked about every slice.
package main

import "fmt"

func minExtraChar(s string, dictionary []string) int64 {
	words := make(map[string]struct{}, len(dictionary))
	for _, w := range dictionary {
		words[w] = struct{}{}
	}
	n := len(s)
	best := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		best[i] = best[i+1] + 1
		for j := i + 1; j <= n; j++ {
			if _, ok := words[s[i:j]]; ok && best[j] < best[i] {
				best[i] = best[j]
			}
		}
	}
	return best[0]
}

var seed int64 = 2707

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%3)
	}
	return string(b)
}

type problem struct {
	s          string
	dictionary []string
}

func main() {
	cases, rounds := 10000, 5
	problems := make([]problem, 0, cases)
	for c := 0; c < cases; c++ {
		s := randomWord(50)
		var dictionary []string
		for w := 0; w < 50; w++ {
			n := nextRandom()%5 + 1
			word := randomWord(n)
			seen := false
			for _, d := range dictionary {
				if d == word {
					seen = true
				}
			}
			if !seen {
				dictionary = append(dictionary, word)
			}
		}
		problems = append(problems, problem{s, dictionary})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range problems {
			extra := minExtraChar(p.s, p.dictionary)
			sum += extra
			check = (check*31 + extra + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d strings of 50 letters against up to 50 words, %d rounds: extra characters sum to %d, checksum %d\n", cases, rounds, sum, check)
}
