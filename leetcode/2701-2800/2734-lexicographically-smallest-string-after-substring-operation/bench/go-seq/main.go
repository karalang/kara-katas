// LeetCode #2734: Lexicographically Smallest String After Substring
// Operation -- the bench (smallest.kara in Go): the run from the first
// letter that is not an 'a' up to the next 'a' moved back a letter,
// edited in a []byte.
package main

import "fmt"

func smallestString(s string) string {
	b := []byte(s)
	n := len(b)
	i := 0
	for i < n && b[i] == 'a' {
		i++
	}
	if i == n {
		b[n-1] = 'z'
	} else {
		for i < n && b[i] != 'a' {
			b[i]--
			i++
		}
	}
	return string(b)
}

var seed int64 = 2734

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 100, 100000, 20
	words := []string{}
	for c := 0; c < count; c++ {
		lead := nextRandom() % (n / 2)
		word := make([]byte, 0, n)
		for k := int64(0); k < n; k++ {
			if k < lead || nextRandom()%5000 == 0 {
				word = append(word, 'a')
			} else {
				word = append(word, byte('b'+nextRandom()%25))
			}
		}
		words = append(words, string(word))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, word := range words {
			answer := smallestString(word)
			var moved int64
			for k := 0; k < len(answer); k++ {
				if answer[k] != word[k] {
					moved++
				}
			}
			sum += moved
			check = (check*31 + moved + int64(answer[len(answer)/2]-'a') + r) % 1000000007
		}
	}
	fmt.Printf("%d words of %d letters, %d rounds: letters moved sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
