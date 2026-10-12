// Benchmark for #409: mirror of longest_palindrome.kara (letter counts).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func longestPalindrome(s string) int64 {
	var counts [128]int64
	for i := 0; i < len(s); i++ {
		counts[s[i]]++
	}
	var length int64
	odd := false
	for i := 0; i < 128; i++ {
		length += counts[i] / 2 * 2
		if counts[i]%2 == 1 {
			odd = true
		}
	}
	if odd {
		return length + 1
	}
	return length
}

var seed int64 = 409

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var queries int64 = 300000
	if len(os.Args) > 1 {
		queries, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	var size int64 = 2000000
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	buf := make([]byte, size)
	for i := range buf {
		buf[i] = letters[step()%52]
	}
	text := string(buf)
	var total, checksum int64
	for q := int64(0); q < queries; q++ {
		n := 1000 + step()%1001
		hi := step()
		lo := step()
		start := (hi*32768 + lo) % (size - n + 1)
		answer := longestPalindrome(text[start : start+n])
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d slices of a %d-letter text: total %d, checksum %d\n", queries, size, total, checksum)
}
