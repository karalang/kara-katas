// LeetCode #1525: Number of Good Ways to Split a String -- bench: the ★
// arm over 200 random strings of 1 to 100000 letters, built once and
// answered 10 times. Each answer takes its own copy of the bytes.
package main

import "fmt"

func numSplits(s string) int64 {
	b := []byte(s)
	n := len(b)
	left := make([]int64, n)
	var seen [26]bool
	var distinct int64
	for i := 0; i < n; i++ {
		c := b[i] - 97
		if !seen[c] {
			seen[c] = true
			distinct++
		}
		left[i] = distinct
	}
	right := make([]int64, n)
	seen = [26]bool{}
	distinct = 0
	for i := n - 1; i >= 0; i-- {
		c := b[i] - 97
		if !seen[c] {
			seen[c] = true
			distinct++
		}
		right[i] = distinct
	}
	var good int64
	for i := 1; i < n; i++ {
		if left[i-1] == right[i] {
			good++
		}
	}
	return good
}

var seed int64 = 1525

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	strs := make([]string, 0, 200)
	for c := 0; c < 200; c++ {
		hi := nextRandom()
		n := (hi*32768+nextRandom())%100000 + 1
		letters := nextRandom()%26 + 1
		buf := make([]byte, 0, n)
		for i := int64(0); i < n; i++ {
			buf = append(buf, byte(97+nextRandom()%letters))
		}
		strs = append(strs, string(buf))
	}
	var check, total int64
	for pass := 0; pass < 10; pass++ {
		for _, s := range strs {
			good := numSplits(s)
			total += good
			check = mix(check, good)
		}
	}
	fmt.Printf("10 passes over 200 strings of up to 100000 letters: %d good splits, checksum %d\n", total, check)
}
