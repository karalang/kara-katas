// LeetCode #1668: Maximum Repeating Substring -- the bench's Go mirror: the
// ★ arm on 400000 problems, words of 1 to 6 letters and sequences of about
// 100 built of whole copies of the word and single letters, all drawn
// first.
package main

import (
	"fmt"
	"strings"
)

func maxRepeating(sequence, word string) int32 {
	var k int32
	repeated := word
	for strings.Contains(sequence, repeated) {
		k++
		repeated += word
	}
	return k
}

var seed int64 = 1668

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n, kinds int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%kinds)
	}
	return string(b)
}

func randomSequence(word string, n int, kinds int64) string {
	var text strings.Builder
	for text.Len() < n {
		if nextRandom()%2 == 0 {
			text.WriteString(word)
		} else {
			text.WriteString(randomText(1, kinds))
		}
	}
	return text.String()
}

func main() {
	const problems = 400000
	type problem struct{ sequence, word string }
	cases := make([]problem, 0, problems)
	for p := 0; p < problems; p++ {
		kinds := nextRandom()%3 + 1
		word := randomText(nextRandom()%6+1, kinds)
		sequence := randomSequence(word, 100, kinds)
		cases = append(cases, problem{sequence, word})
	}
	var total, check int64
	for _, c := range cases {
		k := int64(maxRepeating(c.sequence, c.word))
		total += k
		check = (check*31 + k) % 1000000007
	}
	fmt.Printf("%d problems of about 100 letters: answers sum to %d, checksum %d\n", problems, total, check)
}
