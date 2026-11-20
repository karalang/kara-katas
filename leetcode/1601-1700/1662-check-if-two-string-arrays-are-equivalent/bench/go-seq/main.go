// LeetCode #1662 bench: the ★ arm, two cursors, one in each array.
//
// 20 pairs of word arrays spelling texts of 10^6 letters, cut into words
// of about 8 letters, are built first; half spell the same text and half
// differ in the last letter. Then each pair is checked 20 times.
package main

import "fmt"

func arrayStringsAreEqual(word1, word2 []string) bool {
	w1, i1, w2, i2 := 0, 0, 0, 0
	for w1 < len(word1) && w2 < len(word2) {
		a, b := word1[w1], word2[w2]
		if a[i1] != b[i2] {
			return false
		}
		i1++
		i2++
		if i1 == len(a) {
			w1++
			i1 = 0
		}
		if i2 == len(b) {
			w2++
			i2 = 0
		}
	}
	return w1 == len(word1) && w2 == len(word2)
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int) []byte {
	text := make([]byte, n)
	for i := range text {
		text[i] = byte('a' + nextRandom()%2)
	}
	return text
}

func cut(text []byte) []string {
	var words []string
	start := 0
	for i := 1; i < len(text); i++ {
		if nextRandom()%8 == 0 {
			words = append(words, string(text[start:i]))
			start = i
		}
	}
	return append(words, string(text[start:]))
}

func main() {
	const pairs, letters, rounds = 20, 1000000, 20
	seed = 1662
	type pair struct{ word1, word2 []string }
	var cases []pair
	for k := 0; k < pairs; k++ {
		text := randomText(letters)
		other := append([]byte(nil), text...)
		if k%2 == 1 {
			if other[letters-1] == 'a' {
				other[letters-1] = 'b'
			} else {
				other[letters-1] = 'a'
			}
		}
		cases = append(cases, pair{cut(text), cut(other)})
	}
	equal, check := 0, int64(0)
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			answer := arrayStringsAreEqual(c.word1, c.word2)
			a := int64(1)
			if answer {
				equal++
				a = 2
			}
			check = (check*31 + a + int64(len(c.word1)) + int64(len(c.word2)) + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of %d letters, %d rounds: %d equal, checksum %d\n", pairs, letters, rounds, equal, check)
}
