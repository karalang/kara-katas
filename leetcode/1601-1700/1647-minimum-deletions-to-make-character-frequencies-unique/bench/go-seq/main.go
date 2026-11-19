// LeetCode #1647: Minimum Deletions to Make Character Frequencies Unique
// -- the bench's Go mirror: the ★ arm on 500 random strings of 100000
// letters, each from the first 1 to 26 of the alphabet, all drawn first.
package main

import (
	"fmt"
	"sort"
)

func minDeletions(s string) int32 {
	var counts [26]int32
	for i := 0; i < len(s); i++ {
		counts[s[i]-'a']++
	}
	sort.Slice(counts[:], func(i, j int) bool { return counts[i] > counts[j] })
	var deletions int32
	cap := counts[0]
	for _, c := range counts {
		keep := min(c, cap)
		deletions += c - keep
		cap = max(keep-1, 0)
	}
	return deletions
}

var seed int64 = 1647

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([]string, 0, 500)
	for k := 0; k < 500; k++ {
		letters := nextRandom()%26 + 1
		b := make([]byte, 100000)
		for i := range b {
			b[i] = byte('a' + nextRandom()%letters)
		}
		strings = append(strings, string(b))
	}
	var check, total int64
	for _, s := range strings {
		deletions := int64(minDeletions(s))
		total += deletions
		check = (check*31 + deletions + 1) % 1000000007
	}
	fmt.Printf("500 strings of 100000 letters: deletions sum to %d, checksum %d\n", total, check)
}
