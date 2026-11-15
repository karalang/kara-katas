// LeetCode #2182: Construct String With Repeat Limit -- the benchmark's
// Go mirror of repeat_limit.kara, over a string.
package main

import (
	"fmt"
	"strings"
)

func repeatLimitedString(s string, repeatLimit int64) string {
	var counts [26]int64
	for i := 0; i < len(s); i++ {
		counts[s[i]-97]++
	}
	var out strings.Builder
	var big int64 = 25
	for {
		for big >= 0 && counts[big] == 0 {
			big--
		}
		if big < 0 {
			break
		}
		take := counts[big]
		if repeatLimit < take {
			take = repeatLimit
		}
		for t := int64(0); t < take; t++ {
			out.WriteByte(byte(97 + big))
		}
		counts[big] -= take
		if counts[big] == 0 {
			continue
		}
		small := big - 1
		for small >= 0 && counts[small] == 0 {
			small--
		}
		if small < 0 {
			break
		}
		out.WriteByte(byte(97 + small))
		counts[small]--
	}
	return out.String()
}

var seed int64 = 2182

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]byte, 1000000)
	for i := range row {
		row[i] = byte(97 + nextRandom()%26)
	}
	text := string(row)
	var check int64
	for r := 0; r < 400; r++ {
		a := nextRandom()
		b := nextRandom()
		start := (a*32768 + b) % 900001
		k := nextRandom()%3 + 1
		t := repeatLimitedString(text[start:start+100000], k)
		for i := 0; i < len(t); i++ {
			check = (check*31 + int64(t[i])) % 1000000007
		}
	}
	fmt.Printf("400 solves: checksum %d\n", check)
}
