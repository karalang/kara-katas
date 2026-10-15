// Benchmark for #664: intervals, by their last letter, as the Kara ★ arm.
package main

import "fmt"

func strangePrinter(s string) int64 {
	n := len(s)
	if n == 0 {
		return 0
	}
	turns := make([][]int64, n)
	for i := range turns {
		turns[i] = make([]int64, n)
	}
	for i := n - 1; i >= 0; i-- {
		turns[i][i] = 1
		for j := i + 1; j < n; j++ {
			best := turns[i][j-1] + 1
			for k := i; k < j; k++ {
				if s[k] == s[j] {
					var between int64
					if k+1 <= j-1 {
						between = turns[k+1][j-1]
					}
					if t := turns[i][k] + between; t < best {
						best = t
					}
				}
			}
			turns[i][j] = best
		}
	}
	return turns[0][n-1]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(664)
	texts := make([]string, 0, 64)
	for t := int64(0); t < 64; t++ {
		letters := 2 + t%25
		b := make([]byte, 100)
		for i := range b {
			b[i] = byte(97 + nextRandom(&seed)%letters)
		}
		texts = append(texts, string(b))
	}
	rounds := int64(2000)
	var sum int64
	for r := int64(0); r < rounds; r++ {
		t := strangePrinter(texts[r%64])
		sum = (sum*31 + t + r) % 1000000007
	}
	fmt.Printf("64 texts of 100 letters, %d rounds: checksum %d\n", rounds, sum)
}
