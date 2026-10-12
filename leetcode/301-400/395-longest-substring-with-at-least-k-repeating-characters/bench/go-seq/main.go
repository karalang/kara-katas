// Benchmark for #395: mirror of longest_substring.kara (divide and conquer).
package main

import "fmt"

func longest(b string, lo, hi, k int) int {
	if hi-lo < k {
		return 0
	}
	var count [26]int
	for i := lo; i < hi; i++ {
		count[b[i]-97]++
	}
	best, start, split := 0, lo, false
	for i := lo; i < hi; i++ {
		if count[b[i]-97] < k {
			split = true
			best = max(best, longest(b, start, i, k))
			start = i + 1
		}
	}
	if !split {
		return hi - lo
	}
	return max(best, longest(b, start, hi, k))
}

func longestSubstring(s string, k int) int {
	return longest(s, 0, len(s), k)
}

var seed int64 = 395

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	buf := make([]byte, 1000000)
	for i := range buf {
		x := step() % 26
		y := step() % 26
		buf[i] = byte(min(x, y) + 97)
	}
	pool := string(buf)
	var total, checksum int64
	for n := 0; n < 10000; n++ {
		hi := step()
		a := (hi*32768 + step()) % (1000000 - 10000)
		k := int(1 + step()%30)
		r := int64(longestSubstring(pool[a:a+10000], k))
		total += r
		checksum = (checksum*31 + r) % 1000000007
	}
	fmt.Printf("10000 windows: total %d, checksum %d\n", total, checksum)
}
