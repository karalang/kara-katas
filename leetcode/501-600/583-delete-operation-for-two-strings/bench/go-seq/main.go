// Benchmark for #583: Go mirror of the ★ arm (the longest common
// subsequence); see ../min_distance.kara. Each word is converted to a
// []rune and the table is a slice of slices, as in the Kāra arm.
package main

import "fmt"

func minDistance(word1, word2 string) int64 {
	a := []rune(word1)
	b := []rune(word2)
	m := len(a)
	n := len(b)
	lcs := make([][]int64, m+1)
	for i := range lcs {
		lcs[i] = make([]int64, n+1)
	}
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				lcs[i][j] = lcs[i-1][j-1] + 1
			} else {
				lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])
			}
		}
	}
	return int64(m+n) - 2*lcs[m][n]
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func word(length, letters int64, seed *int64) string {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	s := ""
	for i := int64(0); i < length; i++ {
		k := nextRandom(seed) % letters
		s += alphabet[k : k+1]
	}
	return s
}

func main() {
	var count, rounds int64 = 40, 30
	var seed int64 = 583
	firsts := []string{}
	seconds := []string{}
	for g := int64(0); g < count; g++ {
		letters := 2 + nextRandom(&seed)%25
		firsts = append(firsts, word(500, letters, &seed))
		seconds = append(seconds, word(500, letters, &seed))
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := minDistance(firsts[p], seconds[p])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 500 letters, %d rounds: %d deletions, checksum %d\n", count, rounds, total, checksum)
}
