// LeetCode #1189 bench: the ★ arm in Go, over the same 200 texts of 10^4
// letters and 200 rounds as the Kāra bench.
package main

import (
	"fmt"
	"strings"
)

const rounds = 200

func maxNumberOfBalloons(text string) int64 {
	var count [26]int64
	for i := 0; i < len(text); i++ {
		count[text[i]-'a']++
	}
	letter := func(c byte) int64 { return count[c-'a'] }
	least := letter('b')
	for _, w := range []int64{letter('a'), letter('l') / 2, letter('o') / 2, letter('n')} {
		if w < least {
			least = w
		}
	}
	return least
}

var seed int64 = 1189

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int, letters string) string {
	pool := []rune(letters)
	var b strings.Builder
	b.Grow(n)
	for i := 0; i < n; i++ {
		b.WriteRune(pool[nextRandom()%int64(len(pool))])
	}
	return b.String()
}

func main() {
	alphabets := []string{"abcdefghijklmnopqrstuvwxyz", "balloon", "balonxy"}
	texts := make([]string, 200)
	for i := range texts {
		texts[i] = randomText(10000, alphabets[i%3])
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for _, t := range texts {
			check = (check*131 + maxNumberOfBalloons(t) + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 200 texts of 10000 letters: checksum %d\n", rounds, check)
}
