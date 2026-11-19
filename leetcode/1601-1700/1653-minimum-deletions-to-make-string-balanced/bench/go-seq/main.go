// LeetCode #1653: Minimum Deletions to Make String Balanced -- the bench's
// Go mirror: the ★ arm on 500 random strings of 100000 a's and b's, each
// with its own chance of a b, all drawn first.
package main

import "fmt"

func minimumDeletions(s string) int64 {
	var deletions, bs int64
	for _, c := range s {
		if c == 'b' {
			bs++
		} else {
			deletions = min(deletions+1, bs)
		}
	}
	return deletions
}

var seed int64 = 1653

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([]string, 0, 500)
	for k := 0; k < 500; k++ {
		percent := nextRandom() % 101
		b := make([]byte, 100000)
		for i := range b {
			if nextRandom()%100 < percent {
				b[i] = 'b'
			} else {
				b[i] = 'a'
			}
		}
		strings = append(strings, string(b))
	}
	var check, total int64
	for _, s := range strings {
		deletions := minimumDeletions(s)
		total += deletions
		check = (check*31 + deletions + 1) % 1000000007
	}
	fmt.Printf("500 strings of 100000 letters: deletions sum to %d, checksum %d\n", total, check)
}
