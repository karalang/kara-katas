// LeetCode #712: Minimum ASCII Delete Sum for Two Strings -- a table
// of prefixes.
// Benchmark mirror of the Kara star arm: cost[i][j] is the least ASCII
// sum deleted to make the first i bytes of s1 equal to the first j of
// s2, in a table of rows allocated per call.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func minimumDeleteSum(a, b string) int64 {
	m, n := len(a), len(b)
	cost := make([][]int64, m+1)
	for i := range cost {
		cost[i] = make([]int64, n+1)
	}
	for i := 1; i <= m; i++ {
		cost[i][0] = cost[i-1][0] + int64(a[i-1])
	}
	for j := 1; j <= n; j++ {
		cost[0][j] = cost[0][j-1] + int64(b[j-1])
	}
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				cost[i][j] = cost[i-1][j-1]
			} else {
				dropA := cost[i-1][j] + int64(a[i-1])
				dropB := cost[i][j-1] + int64(b[j-1])
				if dropA < dropB {
					cost[i][j] = dropA
				} else {
					cost[i][j] = dropB
				}
			}
		}
	}
	return cost[m][n]
}

func main() {
	seed := int64(712)
	words := make([]string, 0, 20)
	for w := 0; w < 20; w++ {
		buf := make([]byte, 1000)
		for i := range buf {
			buf[i] = byte(97 + nextRandom(&seed)%26)
		}
		words = append(words, string(buf))
	}
	sum := int64(0)
	for round := 0; round < 10; round++ {
		for p := 0; p < 10; p++ {
			sum += minimumDeleteSum(words[2*p], words[2*p+1])
		}
	}
	fmt.Printf("10 rounds of 10 pairs of 1000 letters: sum %d\n", sum)
}
