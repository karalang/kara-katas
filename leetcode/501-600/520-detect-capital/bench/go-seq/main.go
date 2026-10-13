// Benchmark for #520: Go mirror of the ★ arm (count the capitals); see
// ../detect_capital_use.kara.
package main

import (
	"fmt"
	"strings"
)

func isUpper(c rune) bool { return c >= 'A' && c <= 'Z' }

func detectCapitalUse(word string) bool {
	capitals := 0
	for _, c := range word {
		if isUpper(c) {
			capitals++
		}
	}
	return capitals == 0 || capitals == len(word) || (capitals == 1 && isUpper(rune(word[0])))
}

var seed int64 = 520

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// A random word of 1 to 100 letters: all capitals, all lower case, a
// capital then lower case, any mix, or one of the first three with one
// letter's case turned.
func randomWord() string {
	n := 1 + nextRandom()%100
	kind := nextRandom() % 5
	shape := kind
	if kind == 4 {
		shape = nextRandom() % 3
	}
	letters := make([]byte, n)
	for i := int64(0); i < n; i++ {
		c := byte(97 + nextRandom()%26)
		var capital bool
		switch shape {
		case 0:
			capital = true
		case 1:
			capital = false
		case 2:
			capital = i == 0
		default:
			capital = nextRandom()%2 == 0
		}
		if capital {
			c -= 32
		}
		letters[i] = c
	}
	if kind == 4 {
		at := nextRandom() % n
		if letters[at] >= 'A' && letters[at] <= 'Z' {
			letters[at] += 32
		} else {
			letters[at] -= 32
		}
	}
	var b strings.Builder
	b.Write(letters)
	return b.String()
}

func main() {
	// 20,000 random words made once, then every word checked in each of
	// 200 rounds.
	words := make([]string, 20000)
	for i := range words {
		words[i] = randomWord()
	}
	var right, checksum int64
	for round := int64(0); round < 200; round++ {
		for i, w := range words {
			if detectCapitalUse(w) {
				right++
				checksum = (checksum + (round+1)*(int64(i)+1)) % 1000000007
			}
		}
	}
	fmt.Printf("20000 words, 200 rounds: %d right, checksum %d\n", right, checksum)
}
