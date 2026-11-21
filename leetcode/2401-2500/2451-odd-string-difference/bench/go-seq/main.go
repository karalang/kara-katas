// LeetCode #2451: Odd String Difference -- the bench, the ★ arm: the
// common difference array read off the first three words, and the word
// whose array is not it.
package main

import (
	"fmt"
	"slices"
)

func differences(word string) []int64 {
	var steps []int64
	for j := 1; j < len(word); j++ {
		steps = append(steps, int64(word[j])-int64(word[j-1]))
	}
	return steps
}

func oddString(words []string) string {
	a := differences(words[0])
	b := differences(words[1])
	c := differences(words[2])
	common := b
	if slices.Equal(a, b) || slices.Equal(a, c) {
		common = a
	}
	for _, w := range words {
		if !slices.Equal(differences(w), common) {
			return w
		}
	}
	return words[0]
}

var seed int64 = 2451

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wordOf(steps []int64) string {
	var at, low, high int64
	for _, s := range steps {
		at += s
		low = min(low, at)
		high = max(high, at)
	}
	code := -low + nextRandom()%(26-(high-low))
	letters := []byte{byte(97 + code)}
	for _, s := range steps {
		code += s
		letters = append(letters, byte(97+code))
	}
	return string(letters)
}

func main() {
	var lists [][]string
	for c := 0; c < 2000; c++ {
		common := make([]int64, 19)
		for j := range common {
			common[j] = nextRandom()%3 - 1
		}
		other := append([]int64(nil), common...)
		other[18]++
		odd := nextRandom() % 100
		var words []string
		for i := int64(0); i < 100; i++ {
			if i == odd {
				words = append(words, wordOf(other))
			} else {
				words = append(words, wordOf(common))
			}
		}
		lists = append(lists, words)
	}
	var check int64
	for p := int64(0); p < 110; p++ {
		for c := range lists {
			j := (p + int64(c)) % 100
			lists[c][0], lists[c][j] = lists[c][j], lists[c][0]
			answer := oddString(lists[c])
			for i := 0; i < len(answer); i++ {
				check = (check*31 + int64(answer[i]) + p) % 1000000007
			}
		}
	}
	fmt.Printf("110 passes over 2000 lists of 100 words: checksum %d\n", check)
}
