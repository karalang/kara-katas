// LeetCode #1165: Single-Row Keyboard -- Go mirror of the Kāra ★ arm: each
// letter's place in a table of 26, then the moves summed from place 0.
package main

import "fmt"

func calculateTime(keyboard, word string) int64 {
	var place [26]int64
	for i := 0; i < len(keyboard); i++ {
		place[keyboard[i]-'a'] = int64(i)
	}
	var at, time int64
	for i := 0; i < len(word); i++ {
		next := place[word[i]-'a']
		d := next - at
		if d < 0 {
			d = -d
		}
		time += d
		at = next
	}
	return time
}

var seed int64 = 1165

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	keyboards := make([]string, 16)
	words := make([]string, 16)
	for k := 0; k < 16; k++ {
		b := make([]byte, 26)
		for i := range b {
			b[i] = byte('a' + i)
		}
		for i := 25; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			b[i], b[j] = b[j], b[i]
		}
		keyboards[k] = string(b)
		w := make([]byte, 10000)
		for i := range w {
			w[i] = byte('a' + nextRandom()%26)
		}
		words[k] = string(w)
	}
	var total, check int64
	for r := 0; r < 5000; r++ {
		for k := 0; k < 16; k++ {
			from := nextRandom() % 5000
			t := calculateTime(keyboards[k], words[k][from:])
			total += t
			check = (check*31 + t) % 1000000007
		}
	}
	fmt.Printf("5000 rounds over 16 words of 10^4 letters: total %d, checksum %d\n", total, check)
}
