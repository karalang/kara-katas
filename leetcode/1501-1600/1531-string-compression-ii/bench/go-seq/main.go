// LeetCode #1531: String Compression II -- bench: the ★ arm over 300
// random strings of 1 to 100 letters, each over its own 1 to 4 letters with
// k from 0 to its length, built once and answered 10 times.
package main

import "fmt"

func runLength(count int64) int64 {
	if count == 1 {
		return 1
	} else if count < 10 {
		return 2
	} else if count < 100 {
		return 3
	}
	return 4
}

func getLengthOfOptimalCompression(s string, k int64) int64 {
	n := int64(len(s))
	best := make([][]int64, n+1)
	for i := range best {
		best[i] = make([]int64, k+1)
	}
	for i := n - 1; i >= 0; i-- {
		for j := int64(0); j <= k; j++ {
			shortest := n + 1
			if j > 0 {
				shortest = best[i+1][j-1]
			}
			var same, other int64
			for end := i; end < n; end++ {
				if s[end] == s[i] {
					same++
				} else {
					other++
				}
				if other > j {
					break
				}
				if c := runLength(same) + best[end+1][j-other]; c < shortest {
					shortest = c
				}
			}
			best[i][j] = shortest
		}
	}
	return best[0][k]
}

var seed int64 = 1531

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

type kase struct {
	s string
	k int64
}

func main() {
	cases := make([]kase, 0, 300)
	for c := 0; c < 300; c++ {
		n := nextRandom()%100 + 1
		over := nextRandom()%4 + 1
		b := make([]byte, n)
		for i := int64(0); i < n; i++ {
			b[i] = byte(97 + nextRandom()%over)
		}
		cases = append(cases, kase{string(b), nextRandom() % (n + 1)})
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, c := range cases {
			check = mix(check, getLengthOfOptimalCompression(c.s, c.k))
		}
	}
	fmt.Printf("10 passes over 300 strings of up to 100 letters: checksum %d\n", check)
}
