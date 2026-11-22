// LeetCode #2746: Decremental String Concatenation -- the bench
// (decremental.kara in Go): the shortest string for each pair of first
// and last letters in a 26 by 26 array, rolled word by word.
package main

import "fmt"

const none int64 = 1000000000

func minimizeConcatenatedLength(words []string) int64 {
	var best [26][26]int64
	for f := range best {
		for l := range best[f] {
			best[f][l] = none
		}
	}
	w0 := words[0]
	best[w0[0]-'a'][w0[len(w0)-1]-'a'] = int64(len(w0))
	for _, w := range words[1:] {
		a, b := int(w[0]-'a'), int(w[len(w)-1]-'a')
		n := int64(len(w))
		var next [26][26]int64
		for f := range next {
			for l := range next[f] {
				next[f][l] = none
			}
		}
		for f := 0; f < 26; f++ {
			for l := 0; l < 26; l++ {
				length := best[f][l]
				if length == none {
					continue
				}
				after := length + n
				if l == a {
					after--
				}
				next[f][b] = min(next[f][b], after)
				before := length + n
				if b == f {
					before--
				}
				next[a][l] = min(next[a][l], before)
			}
		}
		best = next
	}
	shortest := none
	for f := range best {
		for l := range best[f] {
			shortest = min(shortest, best[f][l])
		}
	}
	return shortest
}

var seed int64 = 2746

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 100, 5
	lists := [][]string{}
	for k := 0; k < count; k++ {
		words := []string{}
		for i := 0; i < 1000; i++ {
			n := nextRandom()%10 + 1
			w := make([]byte, n)
			for j := range w {
				w[j] = byte('a' + nextRandom()%26)
			}
			words = append(words, string(w))
		}
		lists = append(lists, words)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, words := range lists {
			length := minimizeConcatenatedLength(words)
			sum += length
			check = (check*31 + length + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of 1000 words, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}
