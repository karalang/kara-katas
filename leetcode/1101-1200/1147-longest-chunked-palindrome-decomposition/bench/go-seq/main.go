// LeetCode #1147: Longest Chunked Palindrome Decomposition -- the Go
// mirror of the ★ arm: greedy from both ends, the shortest equal chunks
// taken off, the middle one more.
package main

import "fmt"

func longestDecomposition(t string) int64 {
	i, j, k := 0, len(t), int64(0)
	for i < j {
		size := 1
		for 2*size <= j-i && t[i:i+size] != t[j-size:j] {
			size++
		}
		if 2*size > j-i {
			return k + 1
		}
		k += 2
		i += size
		j -= size
	}
	return k
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func text(seed *int64) string {
	size := int(1 + nextRandom(seed)%4)
	unit := make([]byte, size)
	for u := range unit {
		unit[u] = byte('a' + nextRandom(seed)%2)
	}
	b := make([]byte, 1000)
	for i := range b {
		b[i] = unit[i%size]
	}
	at := nextRandom(seed) % 1000
	b[at] = byte('a' + nextRandom(seed)%2)
	return string(b)
}

func main() {
	seed := int64(1147)
	texts := make([]string, 20)
	for t := range texts {
		texts[t] = text(&seed)
	}
	var total, check int64
	for r := 0; r < 20000; r++ {
		texts[r%20] = text(&seed)
		for _, t := range texts {
			k := longestDecomposition(t)
			total += k
			check = (check*31 + k) % 1000000007
		}
	}
	fmt.Printf("20000 rounds over 20 texts of 1000 letters: chunks total %d, checksum %d\n", total, check)
}
