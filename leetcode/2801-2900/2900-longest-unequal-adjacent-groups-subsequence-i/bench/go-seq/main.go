// LeetCode #2900: Longest Unequal Adjacent Groups Subsequence I -- the
// bench's Go mirror (words.kara): Go strings are immutable and shared,
// so each chosen word is copied through a byte slice to match the
// clones of the other languages.
package main

import "fmt"

var seed int64 = 2900

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func getLongestSubsequence(words []string, groups []int64) []string {
	var chosen []string
	for i := range words {
		if i == 0 || groups[i] != groups[i-1] {
			chosen = append(chosen, string([]byte(words[i])))
		}
	}
	return chosen
}

func main() {
	const count, rounds, n = 10000, 20, 100
	letters := "abcdefghijklmnopqrstuvwxyz"
	cases := make([][]string, count)
	groupsOf := make([][]int64, count)
	for c := 0; c < count; c++ {
		words := make([]string, n)
		for i := 0; i < n; i++ {
			words[i] = string([]byte{letters[nextRandom()%26], letters[i%26], letters[i/26]})
		}
		groups := make([]int64, 0, n)
		group := nextRandom() % 2
		for len(groups) < n {
			run := nextRandom()%5 + 1
			for t := int64(0); t < run; t++ {
				if len(groups) < n {
					groups = append(groups, group)
				}
			}
			group = 1 - group
		}
		cases[c] = words
		groupsOf[c] = groups
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			chosen := getLongestSubsequence(cases[c], groupsOf[c])
			total += int64(len(chosen))
			check = (check*31 + int64(len(chosen)) + r) % 1000000007
			for _, w := range chosen {
				check = (check*31 + int64(len(w))) % 1000000007
			}
			check = (check*31 + int64(chosen[len(chosen)-1][0])) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d, %d rounds: %d words chosen, checksum %d\n", count, n, rounds, total, check)
}
