// LeetCode #2506: Count Pairs Of Similar Strings -- Go mirror of the
// benchmark (similar.kara): the same lists, passes and checksum; the
// masks counted in a map[int64]int64.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2506

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func similarPairs(words []string) int64 {
	seen := map[int64]int64{}
	var pairs int64
	for _, word := range words {
		var mask int64
		for _, ch := range word {
			mask |= 1 << (int64(ch) - 'a')
		}
		pairs += seen[mask]
		seen[mask]++
	}
	return pairs
}

func randomWord() string {
	length := nextRandom()%100 + 1
	letters := nextRandom()%4 + 3
	var b strings.Builder
	for i := int64(0); i < length; i++ {
		b.WriteByte(byte('a' + nextRandom()%letters))
	}
	return b.String()
}

func main() {
	const passes = 24
	lists := make([][]string, 1000)
	for l := range lists {
		lists[l] = make([]string, 100)
		for i := range lists[l] {
			lists[l][i] = randomWord()
		}
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for l := 0; l < 1000; l++ {
			at := check % 100
			was := lists[l][at]
			lists[l][at] = strings.Clone(lists[l][(check/100+p)%100])
			check = (check*31 + similarPairs(lists[l]) + p) % 1000000007
			lists[l][at] = was
		}
	}
	fmt.Printf("%d passes over 1000 lists of 100 words: checksum %d\n", passes, check)
}
