// LeetCode #2490: Circular Sentence -- Go mirror of the ★ arm's benchmark
// (circular.kara): the same 200 sentences and 2300 passes, each letter
// changed and changed back, the sentence made a fresh `string` for every
// answer.
package main

import "fmt"

func isCircularSentence(s string) bool {
	n := len(s)
	if s[0] != s[n-1] {
		return false
	}
	for i := 1; i < n-1; i++ {
		if s[i] == ' ' && s[i-1] != s[i+1] {
			return false
		}
	}
	return true
}

var seed int64 = 2490

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letter(k int64) byte { return byte('a' + k%26) }

func sentence() []byte {
	text := []byte{}
	first := letter(nextRandom())
	last := first
	for len(text) < 490 {
		if len(text) > 0 {
			text = append(text, ' ')
		}
		text = append(text, last)
		extra := nextRandom() % 8
		for i := int64(0); i < extra; i++ {
			text = append(text, letter(nextRandom()))
		}
		last = text[len(text)-1]
	}
	return append(text, ' ', last, first)
}

func main() {
	passes := int64(2300)
	sentences := make([][]byte, 200)
	for s := range sentences {
		sentences[s] = sentence()
	}
	check := int64(0)
	circular := int64(0)
	for p := int64(0); p < passes; p++ {
		for s := 0; s < 200; s++ {
			n := int64(len(sentences[s]))
			at := check % n
			was := sentences[s][at]
			if was != ' ' {
				sentences[s][at] = letter(check/n + p)
			}
			answer := isCircularSentence(string(sentences[s]))
			sentences[s][at] = was
			if answer {
				circular++
			}
			v := int64(2)
			if answer {
				v = 1
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 200 sentences: %d circular, checksum %d\n", passes, circular, check)
}
