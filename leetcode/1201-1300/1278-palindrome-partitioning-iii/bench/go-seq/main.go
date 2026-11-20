// LeetCode #1278 bench, in Go: the ★ arm (the changes for every
// substring, then the fewest for each prefix in each number of pieces) on
// 200 random strings of 100 letters from 2 to 26, each cut into 1 to 100
// pieces, drawn once; 20 rounds, every answer folded into a checksum.
package main

import "fmt"

func palindromePartition(s string, k int) int64 {
	c := []rune(s)
	n := len(c)
	cost := make([][]int64, n)
	for i := range cost {
		cost[i] = make([]int64, n)
	}
	for length := 2; length <= n; length++ {
		for i := 0; i+length-1 < n; i++ {
			j := i + length - 1
			var inner int64
			if length > 2 {
				inner = cost[i+1][j-1]
			}
			if c[i] != c[j] {
				inner++
			}
			cost[i][j] = inner
		}
	}
	unreachable := int64(n + 1)
	best := make([][]int64, k+1)
	for p := range best {
		best[p] = make([]int64, n+1)
		for j := range best[p] {
			best[p][j] = unreachable
		}
	}
	best[0][0] = 0
	for p := 1; p <= k; p++ {
		for j := p; j <= n; j++ {
			for i := p - 1; i < j; i++ {
				through := best[p-1][i] + cost[i][j-1]
				if through < best[p][j] {
					best[p][j] = through
				}
			}
		}
	}
	return best[k][n]
}

var seed int64 = 1278

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	strs := make([]string, 0, 200)
	ks := make([]int, 0, 200)
	for c := 0; c < 200; c++ {
		letters := nextRandom()%25 + 2
		b := make([]byte, 100)
		for x := range b {
			b[x] = alphabet[nextRandom()%letters]
		}
		strs = append(strs, string(b))
		ks = append(ks, int(nextRandom()%100+1))
	}
	var check int64
	for round := int64(0); round < 20; round++ {
		for c := range strs {
			check = (check*131 + palindromePartition(strs[c], ks[c]) + round) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 200 strings of 100 letters: checksum %d\n", check)
}
