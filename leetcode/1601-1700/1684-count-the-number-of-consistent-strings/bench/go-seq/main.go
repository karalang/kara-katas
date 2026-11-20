// LeetCode #1684: Count the Number of Consistent Strings -- the bench's Go
// mirror: the ★ arm on 100 random problems of 10000 words, all drawn first,
// each answered 20 times.
package main

import (
	"fmt"
	"strings"
)

func countConsistent(allowed string, words []string) int32 {
	var ok [26]bool
	for i := 0; i < len(allowed); i++ {
		ok[allowed[i]-'a'] = true
	}
	var count int32
	for _, word := range words {
		all := true
		for i := 0; i < len(word); i++ {
			if !ok[word[i]-'a'] {
				all = false
				break
			}
		}
		if all {
			count++
		}
	}
	return count
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1684

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	allowed string
	words   []string
}

func main() {
	const count, size, rounds = 100, 10000, 20
	const alphabet = "abcdefghijklmnopqrstuvwxyz"
	problems := make([]problem, 0, count)
	for c := 0; c < count; c++ {
		var allowed strings.Builder
		for i := 0; i < 26; i++ {
			if nextRandom()%8 != 0 {
				allowed.WriteByte(alphabet[i])
			}
		}
		if allowed.Len() == 0 {
			allowed.WriteByte('a')
		}
		words := make([]string, 0, size)
		for w := 0; w < size; w++ {
			length := nextRandom()%10 + 1
			var word strings.Builder
			for i := int64(0); i < length; i++ {
				word.WriteByte(alphabet[nextRandom()%26])
			}
			words = append(words, word.String())
		}
		problems = append(problems, problem{allowed.String(), words})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			answer := int64(countConsistent(p.allowed, p.words))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d words, %d rounds: %d consistent, checksum %d\n", count, size, rounds, total, check)
}
