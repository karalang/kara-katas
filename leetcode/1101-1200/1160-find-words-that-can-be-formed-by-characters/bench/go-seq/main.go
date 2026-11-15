// LeetCode #1160 bench: the ★ arm's counts of each letter, the same
// workload as count_characters.kara.
package main

import "fmt"

func countCharacters(words []string, chars string) int64 {
	var have [26]int64
	for i := 0; i < len(chars); i++ {
		have[chars[i]-'a']++
	}
	var total int64
	for _, w := range words {
		var need [26]int64
		good := true
		for i := 0; i < len(w); i++ {
			c := w[i] - 'a'
			need[c]++
			if need[c] > have[c] {
				good = false
				break
			}
		}
		if good {
			total += int64(len(w))
		}
	}
	return total
}

var seed int64 = 1160

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(n, k int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%k)
	}
	return string(b)
}

func main() {
	const passes = 1500
	type problem struct {
		words []string
		chars string
	}
	var problems []problem
	for p := 0; p < 12; p++ {
		kind := p % 3
		k := int64(26)
		if kind == 1 {
			k = 4
		}
		chars := word(100, k)
		words := make([]string, 0, 1000)
		for i := 0; i < 1000; i++ {
			if kind == 0 {
				words = append(words, word(1+nextRandom()%100, 26))
			} else if kind == 1 {
				words = append(words, word(1+nextRandom()%30, 4))
			} else {
				var b []byte
				for j := 0; j < len(chars); j++ {
					if nextRandom()%2 == 0 {
						b = append(b, chars[j])
					}
				}
				if i%2 == 1 {
					b = append(b, b[nextRandom()%int64(len(b))])
				}
				words = append(words, string(b))
			}
		}
		problems = append(problems, problem{words, chars})
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, pr := range problems {
			check = (check*31 + countCharacters(pr.words, pr.chars) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 12 problems of 1000 words: checksum %d\n", passes, check)
}
