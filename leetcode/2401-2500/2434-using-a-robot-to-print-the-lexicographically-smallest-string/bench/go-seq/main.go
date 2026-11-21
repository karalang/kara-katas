// LeetCode #2434: Using a Robot to Print the Lexicographically Smallest
// String -- the bench, the ★ arm: the letters left counted, a pointer at
// the smallest with a count, and `t` popped after each push while its
// top is no larger.
package main

import "fmt"

func robotWithString(b []byte) []byte {
	var left [26]int64
	for _, c := range b {
		left[c-'a']++
	}
	smallest := 0
	var t, paper []byte
	for _, c := range b {
		t = append(t, c)
		left[c-'a']--
		for smallest < 26 && left[smallest] == 0 {
			smallest++
		}
		for len(t) > 0 && int(t[len(t)-1]-'a') <= smallest {
			paper = append(paper, t[len(t)-1])
			t = t[:len(t)-1]
		}
	}
	return paper
}

var seed int64 = 2434

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	word := make([]byte, 0)
	for i := 0; i < 100000; i++ {
		word = append(word, byte('a'+nextRandom()%8))
	}
	var check int64
	for p := int64(0); p < 300; p++ {
		word[(p*7919)%100000] = byte('a' + p%8)
		paper := robotWithString(word)
		for _, c := range paper {
			check = (check*31 + int64(c)) % 1000000007
		}
	}
	fmt.Printf("300 passes over 10^5 letters: checksum %d\n", check)
}
