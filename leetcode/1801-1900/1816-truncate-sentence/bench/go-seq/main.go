// LeetCode #1816: Truncate Sentence -- the bench in Go: the ★ arm over
// 2 * 10^6 calls on 1000 sentences of 20 to 100 words, built once, each
// sentence and its k drawn from the checksum so far.
package main

import (
	"fmt"
	"strings"
)

func truncateSentence(s string, k int64) string {
	words := strings.SplitN(s, " ", int(k)+1)
	if int64(len(words)) > k {
		words = words[:k]
	}
	return strings.Join(words, " ")
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1816)
	sentences := make([]string, 0, 1000)
	wordsIn := make([]int64, 0, 1000)
	for i := 0; i < 1000; i++ {
		n := 20 + nextRandom(&seed)%81
		words := make([]string, 0, n)
		for w := int64(0); w < n; w++ {
			m := 1 + nextRandom(&seed)%5
			b := make([]byte, 0, m)
			for c := int64(0); c < m; c++ {
				b = append(b, byte(97+nextRandom(&seed)%26))
			}
			words = append(words, string(b))
		}
		sentences = append(sentences, strings.Join(words, " "))
		wordsIn = append(wordsIn, n)
	}
	var check int64
	for call := int64(0); call < 2000000; call++ {
		i := (check + call) % 1000
		cut := truncateSentence(sentences[i], 1+(check+call)%wordsIn[i])
		check = (check*31 + int64(len(cut))) % 1000000007
	}
	fmt.Printf("2000000 calls: checksum %d\n", check)
}
