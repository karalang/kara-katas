// LeetCode #903: Valid Permutations for DI Sequence -- bench program, Go.
//
// Ranks of the last number with running sums, over one string of 4,000
// random letters built once. Each round counts its valid permutations,
// folds the count into a checksum and flips one letter.
package main

import "fmt"

func numPermsDISequence(s string) int64 {
	var m int64 = 1000000007
	n := len(s)
	ways := []int64{1}
	for i := 1; i <= n; i++ {
		below := make([]int64, i+1)
		for k := 0; k < i; k++ {
			below[k+1] = (below[k] + ways[k]) % m
		}
		next := make([]int64, i+1)
		for j := 0; j <= i; j++ {
			if s[i-1] == 'I' {
				next[j] = below[j]
			} else {
				next[j] = (below[i] - below[j] + m) % m
			}
		}
		ways = next
	}
	var total int64
	for _, w := range ways {
		total = (total + w) % m
	}
	return total
}

var seed int64 = 903

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	length := 4000
	rounds := 12
	letters := make([]byte, length)
	for i := range letters {
		if nextRandom()%2 == 0 {
			letters[i] = 'D'
		} else {
			letters[i] = 'I'
		}
	}
	var check int64
	for r := 0; r < rounds; r++ {
		got := numPermsDISequence(string(letters))
		check = (check*31 + got) % 1000000007
		at := r * 7919 % length
		if letters[at] == 'D' {
			letters[at] = 'I'
		} else {
			letters[at] = 'D'
		}
	}
	fmt.Printf("%d rounds over %d letters: checksum %d\n", rounds, length, check)
}
