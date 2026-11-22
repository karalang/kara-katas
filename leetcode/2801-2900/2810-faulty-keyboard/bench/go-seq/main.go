// LeetCode #2810: Faulty Keyboard -- the bench in Go: the ★ arm over 20000
// strings of 100 letters, about a fifth of them i, all drawn first, then
// each typed 10 times; the screen a []byte, a fresh one made at each i.
package main

import "fmt"

func finalString(s string) string {
	screen := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		if s[i] == 'i' {
			turned := make([]byte, len(screen), len(s))
			for k := range screen {
				turned[k] = screen[len(screen)-1-k]
			}
			screen = turned
		} else {
			screen = append(screen, s[i])
		}
	}
	return string(screen)
}

var seed int64 = 2810

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func digest(s string) int64 {
	var h int64
	for i := 0; i < len(s); i++ {
		h = (h*131 + int64(s[i])) % 1000000007
	}
	return h
}

func main() {
	count := 20000
	rounds := 10
	letters := "abcdefghijklmnopqrstuvwxyz"
	cases := make([]string, count)
	for c := range cases {
		b := make([]byte, 100)
		for k := range b {
			r := nextRandom() % 125
			if r < 25 {
				b[k] = 'i'
			} else {
				b[k] = letters[r%26]
			}
		}
		cases[c] = string(b)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, s := range cases {
			out := finalString(s)
			total += int64(len(out))
			check = (check*31 + digest(out) + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of 100, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, total, check)
}
