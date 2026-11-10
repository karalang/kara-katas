// LeetCode #2083: Substrings That Begin and End With the Same Letter --
// Go mirror of the ★ arm's benchmark (same.kara): one text of 10^6
// letters built once, then 5000 windows of 10^5 letters counted through a
// substring of the text, which shares its bytes.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2083

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func numberOfSubstrings(s string) int64 {
	var counts [26]int64
	for i := 0; i < len(s); i++ {
		counts[s[i]-'a']++
	}
	var total int64
	for _, c := range counts {
		total += c * (c + 1) / 2
	}
	return total
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	var b strings.Builder
	for i := 0; i < 1000000; i++ {
		at := nextRandom() % 26
		at = at * (nextRandom() % 26) / 25
		b.WriteString(letters[at : at+1])
	}
	text := b.String()
	var total, check int64
	for i := 0; i < 5000; i++ {
		from := nextRandom() * 32768
		from = (from + nextRandom()) % 900001
		a := numberOfSubstrings(text[from : from+100000])
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("5000 windows: sum %d, checksum %d\n", total, check)
}
