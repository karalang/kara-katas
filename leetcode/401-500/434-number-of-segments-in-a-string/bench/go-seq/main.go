// Benchmark for #434: mirror of count_segments.kara (counting starts)
// on 10,000 windows of one random text of 1,000,000 characters.
package main

import (
	"fmt"
	"strings"
)

func countSegments(s string) int64 {
	var count int64
	for i := 0; i < len(s); i++ {
		if s[i] != ' ' && (i == 0 || s[i-1] == ' ') {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const size int64 = 1000000
	const windows = 10000
	seed := int64(434)
	letters := "abcdefghijklmnopqrstuvwxyz"
	// Words of 1 to 8 letters between runs of 1 to 3 spaces.
	var b strings.Builder
	for int64(b.Len()) < size {
		word := 1 + nextRandom(&seed)%8
		for k := int64(0); k < word; k++ {
			if int64(b.Len()) < size {
				b.WriteByte(letters[nextRandom(&seed)%26])
			}
		}
		gap := 1 + nextRandom(&seed)%3
		for k := int64(0); k < gap; k++ {
			if int64(b.Len()) < size {
				b.WriteByte(' ')
			}
		}
	}
	text := b.String()
	var total, checksum int64
	for w := 0; w < windows; w++ {
		length := nextRandom(&seed) % 100001
		start := nextRandom(&seed) % (size - length + 1)
		n := countSegments(text[start : start+length])
		total += n
		checksum = (checksum*31 + n) % 1000000007
	}
	fmt.Printf("%d windows of a text of %d: %d segments, checksum %d\n", windows, size, total, checksum)
}
