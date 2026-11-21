// LeetCode #2452: Words Within Two Edits of Dictionary -- the bench, the
// ★ arm: each query against each word, the differing places counted
// until a third rules the word out.
package main

import "fmt"

func withinTwo(a, b string) bool {
	differ := 0
	for j := 0; j < len(a); j++ {
		if a[j] != b[j] {
			differ++
			if differ > 2 {
				return false
			}
		}
	}
	return true
}

func twoEditWords(queries, dictionary []string) []string {
	var answers []string
	for _, q := range queries {
		for _, w := range dictionary {
			if withinTwo(q, w) {
				answers = append(answers, q)
				break
			}
		}
	}
	return answers
}

var seed int64 = 2452

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord() []byte {
	b := make([]byte, 100)
	for i := range b {
		b[i] = byte(97 + nextRandom()%4)
	}
	return b
}

func main() {
	var dictionaries [][]string
	var queries [][][]byte
	for c := 0; c < 100; c++ {
		words := make([][]byte, 100)
		for i := range words {
			words[i] = randomWord()
		}
		var asks [][]byte
		for i := 0; i < 100; i++ {
			b := append([]byte(nil), words[nextRandom()%100]...)
			changes := nextRandom() % 5
			for t := int64(0); t < changes; t++ {
				place := nextRandom() % 100
				b[place] = byte(97 + nextRandom()%4)
			}
			asks = append(asks, b)
		}
		var dict []string
		for _, w := range words {
			dict = append(dict, string(w))
		}
		dictionaries = append(dictionaries, dict)
		queries = append(queries, asks)
	}
	var check int64
	for p := int64(0); p < 45; p++ {
		for c := 0; c < 100; c++ {
			place := nextRandom() % 100
			queries[c][p%100][place] = byte(97 + nextRandom()%4)
			var asks []string
			for _, q := range queries[c] {
				asks = append(asks, string(q))
			}
			kept := twoEditWords(asks, dictionaries[c])
			check = (check*31 + int64(len(kept)) + p) % 1000000007
		}
	}
	fmt.Printf("45 passes over 100 cases of 100 queries: checksum %d\n", check)
}
