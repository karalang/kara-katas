// LeetCode 748 — Shortest Completing Word, bench: the ★ arm (letter
// counts) on a list of 1000 words that keeps changing, against a new
// plate each round. Mirrors shortest_completing_word.kara.
package main

import "fmt"

func shortestCompletingWord(plate string, words []string) string {
	var need [26]int64
	for i := 0; i < len(plate); i++ {
		c := plate[i]
		if c >= 'a' && c <= 'z' {
			need[c-'a']++
		} else if c >= 'A' && c <= 'Z' {
			need[c-'A']++
		}
	}
	best := -1
	for i, w := range words {
		if best != -1 && len(w) >= len(words[best]) {
			continue
		}
		var have [26]int64
		for k := 0; k < len(w); k++ {
			have[w[k]-'a']++
		}
		complete := true
		for c := 0; c < 26; c++ {
			if have[c] < need[c] {
				complete = false
			}
		}
		if complete {
			best = i
		}
	}
	return words[best]
}

var seed int64 = 748

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord() string {
	n := 1 + nextRandom()%15
	b := make([]byte, n)
	for k := range b {
		b[k] = byte(97 + nextRandom()%6)
	}
	return string(b)
}

func randomPlate() string {
	n := 1 + nextRandom()%7
	b := make([]byte, n)
	for k := range b {
		kind := nextRandom() % 6
		var code int64
		if kind < 2 {
			code = 97 + nextRandom()%6
		} else if kind < 4 {
			code = 65 + nextRandom()%6
		} else if kind == 4 {
			code = 48 + nextRandom()%10
		} else {
			code = 32
		}
		b[k] = byte(code)
	}
	return string(b)
}

func main() {
	const rounds = 100000
	const n = 1000
	words := make([]string, n)
	for i := range words {
		words[i] = randomWord()
	}
	var letters, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < 5; c++ {
			words[nextRandom()%(n-1)] = randomWord()
		}
		plate := randomPlate()
		last := make([]byte, 0, 7)
		for k := 0; k < len(plate); k++ {
			c := plate[k]
			if c >= 'a' && c <= 'z' {
				last = append(last, c)
			} else if c >= 'A' && c <= 'Z' {
				last = append(last, c+32)
			}
		}
		if len(last) == 0 {
			last = append(last, 'a')
		}
		words[n-1] = string(last)
		got := shortestCompletingWord(plate, words)
		letters += int64(len(got))
		for k := 0; k < len(got); k++ {
			check = (check*31 + int64(got[k])) % 1000000007
		}
	}
	fmt.Printf("%d plates against 1000 words: answers %d letters long in all, checksum %d\n", rounds, letters, check)
}
