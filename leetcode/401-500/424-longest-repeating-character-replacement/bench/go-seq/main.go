// Benchmark for #424: mirror of character_replacement.kara (a window
// that never shrinks).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func characterReplacement(s string, k int64) int64 {
	var count [26]int64
	var best int64
	left := 0
	for right := 0; right < len(s); right++ {
		c := s[right] - 'A'
		count[c]++
		best = max(best, count[c])
		if int64(right-left+1)-best > k {
			count[s[left]-'A']--
			left++
		}
	}
	return int64(len(s) - left)
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	calls := int64(3000)
	if len(os.Args) > 1 {
		calls, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	size := int64(1000000)
	seed := int64(424)
	text := make([]byte, 0, size)
	for int64(len(text)) < size {
		letter := byte('A' + step(&seed)%5)
		run := 1 + step(&seed)%8
		for i := int64(0); i < run; i++ {
			if int64(len(text)) < size {
				text = append(text, letter)
			}
		}
	}
	s := string(text)
	var total, checksum int64
	for c := int64(0); c < calls; c++ {
		length := 10000 + step(&seed)*3%90000
		start := step(&seed) * 30 % (size - length)
		k := step(&seed) % 50
		answer := characterReplacement(s[start:start+length], k)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
