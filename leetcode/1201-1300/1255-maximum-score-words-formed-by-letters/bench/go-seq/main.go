// LeetCode #1255 bench, in Go: the ★ arm (backtracking, every word in turn
// left out or, when the letters on hand cover it, taken) on 100 random
// cases built once, each 14 words of 1 to 15 letters and 100 letters to
// spend from the first 6 letters of the alphabet; each asked 3 times,
// every best score folded into a checksum.
package main

import "fmt"

var seed int64 = 1255

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func best(i int, words [][]int64, left []int64, score []int64) int64 {
	if i == len(words) {
		return 0
	}
	top := best(i+1, words, left, score)
	need := append([]int64(nil), words[i]...)
	fits := true
	for c := 0; c < 26; c++ {
		if need[c] > left[c] {
			fits = false
			break
		}
	}
	if fits {
		for c := 0; c < 26; c++ {
			left[c] -= need[c]
		}
		var gain int64
		for c := 0; c < 26; c++ {
			gain += need[c] * score[c]
		}
		if with := gain + best(i+1, words, left, score); with > top {
			top = with
		}
		for c := 0; c < 26; c++ {
			left[c] += need[c]
		}
	}
	return top
}

func maxScoreWords(words []string, letters []byte, score []int64) int64 {
	counts := make([][]int64, len(words))
	for w, word := range words {
		counts[w] = make([]int64, 26)
		for k := 0; k < len(word); k++ {
			counts[w][word[k]-'a']++
		}
	}
	left := make([]int64, 26)
	for _, ch := range letters {
		left[ch-'a']++
	}
	return best(0, counts, left, score)
}

type caseT struct {
	words   []string
	letters []byte
	score   []int64
}

func main() {
	cases := make([]caseT, 0, 100)
	for t := 0; t < 100; t++ {
		words := make([]string, 0, 14)
		for w := 0; w < 14; w++ {
			n := nextRandom()%15 + 1
			b := make([]byte, n)
			for k := range b {
				b[k] = byte('a' + nextRandom()%6)
			}
			words = append(words, string(b))
		}
		letters := make([]byte, 100)
		for k := range letters {
			letters[k] = byte('a' + nextRandom()%6)
		}
		score := make([]int64, 26)
		for c := range score {
			score[c] = nextRandom() % 11
		}
		cases = append(cases, caseT{words, letters, score})
	}
	var check int64
	for r := 0; r < 3; r++ {
		for _, c := range cases {
			check = (check*131 + maxScoreWords(c.words, c.letters, c.score)) % 1000000007
		}
	}
	fmt.Printf("3 rounds of 100 cases of 14 words: checksum %d\n", check)
}
