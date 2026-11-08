// LeetCode #2014: Longest Subsequence Repeated k Times -- the ★ arm's
// benchmark, a mirror of longest.kara.
package main

import "fmt"

func repeats(s, t []byte, k int64) bool {
	i := 0
	var found int64
	for _, c := range s {
		if c == t[i] {
			i++
			if i == len(t) {
				found++
				if found == k {
					return true
				}
				i = 0
			}
		}
	}
	return false
}

func longestSubsequenceRepeatedK(s []byte, k int64) []byte {
	var counts [26]int64
	for _, c := range s {
		counts[c-'a']++
	}
	var letters []byte
	for i := 0; i < 26; i++ {
		if counts[i] >= k {
			letters = append(letters, byte('a'+i))
		}
	}
	queue := [][]byte{{}}
	var best []byte
	for len(queue) > 0 {
		t := queue[0]
		queue = queue[1:]
		for _, c := range letters {
			next := make([]byte, len(t)+1)
			copy(next, t)
			next[len(t)] = c
			if repeats(s, next, k) {
				best = append([]byte(nil), next...)
				queue = append(queue, next)
			}
		}
	}
	return best
}

var seed int64 = 2014

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int, letters int64) []byte {
	width := nextRandom()%7 + 1
	pattern := make([]byte, 0, width)
	for i := int64(0); i < width; i++ {
		pattern = append(pattern, byte('a'+nextRandom()%letters))
	}
	text := make([]byte, 0, n)
	at := 0
	for len(text) < n {
		if nextRandom()%10 < 9 {
			text = append(text, pattern[at])
		}
		if len(text) < n && nextRandom()%10 < 1 {
			text = append(text, byte('a'+nextRandom()%letters))
		}
		at = (at + 1) % len(pattern)
	}
	return text
}

func main() {
	texts := make([][]byte, 200)
	ks := make([]int64, 200)
	for c := 0; c < 200; c++ {
		ks[c] = 251 + nextRandom()%50
		texts[c] = randomText(2000, int64(c%8+2))
	}
	var calls, total, check int64
	for r := 0; r < 5; r++ {
		for c := 0; c < 200; c++ {
			answer := longestSubsequenceRepeatedK(texts[c], ks[c])
			calls++
			total += int64(len(answer))
			for _, ch := range answer {
				check = (check*31 + int64(ch)) % 1000000007
			}
			check = (check*31 + int64(len(answer))) % 1000000007
		}
	}
	fmt.Printf("%d calls: total length %d, checksum %d\n", calls, total, check)
}
