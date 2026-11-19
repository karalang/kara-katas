// LeetCode #1638: Count Substrings That Differ by One Character -- the
// bench's Go mirror: the ★ arm on 5000 random pairs of 100-letter words
// over the letters a to c, all drawn first.
package main

import "fmt"

func countSubstrings(s, t string) int64 {
	n, m := len(s), len(t)
	left := make([][]int64, n+1)
	right := make([][]int64, n+1)
	for i := range left {
		left[i] = make([]int64, m+1)
		right[i] = make([]int64, m+1)
	}
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if s[i] == t[j] {
				left[i+1][j+1] = left[i][j] + 1
			}
		}
	}
	for i := n - 1; i >= 0; i-- {
		for j := m - 1; j >= 0; j-- {
			if s[i] == t[j] {
				right[i][j] = right[i+1][j+1] + 1
			}
		}
	}
	var count int64
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if s[i] != t[j] {
				count += (left[i][j] + 1) * (right[i+1][j+1] + 1)
			}
		}
	}
	return count
}

var seed int64 = 1638

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord() string {
	word := make([]byte, 100)
	for i := range word {
		word[i] = byte('a' + nextRandom()%3)
	}
	return string(word)
}

func main() {
	pairs := make([][2]string, 5000)
	for i := range pairs {
		s := randomWord()
		t := randomWord()
		pairs[i] = [2]string{s, t}
	}
	var check, total int64
	for _, pair := range pairs {
		count := countSubstrings(pair[0], pair[1])
		total += count
		check = (check*31 + count + 1) % 1000000007
	}
	fmt.Printf("5000 pairs of 100 letters: counts sum to %d, checksum %d\n", total, check)
}
