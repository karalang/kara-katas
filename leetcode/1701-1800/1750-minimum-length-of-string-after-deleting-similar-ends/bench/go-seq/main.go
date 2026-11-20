// LeetCode #1750: Minimum Length of String After Deleting Similar Ends --
// the bench (ends.kara in Go): two pointers.
package main

import (
	"fmt"
	"strings"
)

func minimumLength(s string) int32 {
	left, right := 0, len(s)-1
	for left < right && s[left] == s[right] {
		c := s[left]
		for left <= right && s[left] == c {
			left++
		}
		for right >= left && s[right] == c {
			right--
		}
	}
	return int32(right - left + 1)
}

var seed int64 = 1750

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a random middle of up to 1000 letters from `a` and `b`, wrapped in
// layers of one letter on both sides until the string is `n` long
func draw(n int64) string {
	const alphabet = "ab"
	var middle strings.Builder
	m := nextRandom() % 1000
	for i := int64(0); i < m; i++ {
		k := nextRandom() % 2
		middle.WriteString(alphabet[k : k+1])
	}
	var front []string
	var back strings.Builder
	size := int64(middle.Len())
	for size < n {
		k := nextRandom() % 2
		letter := alphabet[k : k+1]
		before := nextRandom()%3 + 1
		after := nextRandom()%3 + 1
		front = append(front, strings.Repeat(letter, int(before)))
		back.WriteString(strings.Repeat(letter, int(after)))
		size += before + after
	}
	var s strings.Builder
	for i := len(front) - 1; i >= 0; i-- {
		s.WriteString(front[i])
	}
	s.WriteString(middle.String())
	s.WriteString(back.String())
	return s.String()
}

func main() {
	const count, rounds, n = 50, 40, 100000
	strs := make([]string, count)
	for c := range strs {
		strs[c] = draw(n)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range strs {
			answer := int64(minimumLength(s))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of about %d letters, %d rounds: lengths add to %d, checksum %d\n", count, n, rounds, sum, check)
}
