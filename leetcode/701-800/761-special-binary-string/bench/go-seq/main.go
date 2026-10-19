// LeetCode 761 — Special Binary String: benchmark, the ★ arm in Go.
// 200,000 random special strings of 50 characters.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func makeLargestSpecial(s string) string {
	var mountains []string
	depth, start := 0, 0
	for i := 0; i < len(s); i++ {
		if s[i] == '1' {
			depth++
		} else {
			depth--
		}
		if depth == 0 {
			mountains = append(mountains, "1"+makeLargestSpecial(s[start+1:i])+"0")
			start = i + 1
		}
	}
	sort.Slice(mountains, func(a, b int) bool { return mountains[a] > mountains[b] })
	return strings.Join(mountains, "")
}

var seed int64 = 761

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 200000
	var leading, check int64
	for r := 0; r < rounds; r++ {
		b := make([]byte, 50)
		ones, depth := 0, 0
		for i := 0; i < 50; i++ {
			if ones < 25 && (depth == 0 || nextRandom()%2 == 0) {
				b[i] = '1'
				ones++
				depth++
			} else {
				b[i] = '0'
				depth--
			}
		}
		largest := makeLargestSpecial(string(b))
		lead := true
		for i := 0; i < len(largest); i++ {
			if largest[i] == '0' {
				lead = false
			}
			if lead {
				leading++
			}
			var bit int64
			if largest[i] == '1' {
				bit = 1
			}
			check = (check*2 + bit) % 1000000007
		}
	}
	fmt.Printf("%d strings of 50 characters: %d leading 1s, checksum %d\n", rounds, leading, check)
}
