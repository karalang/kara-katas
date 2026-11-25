// LeetCode #1370 bench -- Go: the letters counted, then sweeps up from a
// to z and down from z to a, each taking one of every letter still left,
// until none is.
package main

import (
	"fmt"
	"strings"
)

func sortString(s string) string {
	var counts [26]int64
	for k := 0; k < len(s); k++ {
		counts[s[k]-'a']++
	}
	var out strings.Builder
	left := len(s)
	for left > 0 {
		for i := 0; i < 26; i++ {
			if counts[i] > 0 {
				out.WriteByte(byte('a' + i))
				counts[i]--
				left--
			}
		}
		for i := 25; i >= 0; i-- {
			if counts[i] > 0 {
				out.WriteByte(byte('a' + i))
				counts[i]--
				left--
			}
		}
	}
	return out.String()
}

var seed int64 = 1370

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 strings of 500 letters, the constraints' most, each from the
	// first 2 to 26 letters of the alphabet, built once; then 60000
	// rounds, each changing one letter of one string and sorting that
	// string, all drawn from the checksum so far
	strs := make([]string, 20)
	for k := int64(0); k < 20; k++ {
		letters := 2 + k*24/19
		b := make([]byte, 500)
		for j := range b {
			b[j] = byte('a' + nextRandom()%letters)
		}
		strs[k] = string(b)
	}
	var check int64
	for r := int64(0); r < 60000; r++ {
		i := check % 20
		at := (check / 20) % 500
		b := []byte(strs[i])
		b[at] = byte('a' + (check/10000)%26)
		strs[i] = string(b)
		sorted := sortString(strs[i])
		for k := 0; k < len(sorted); k++ {
			check = (check*31 + int64(sorted[k])) % 1000000007
		}
		check = (check + r) % 1000000007
	}
	fmt.Printf("60000 rounds over 20 strings of 500 letters: checksum %d\n", check)
}
