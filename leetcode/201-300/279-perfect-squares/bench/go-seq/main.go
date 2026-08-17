// LeetCode 279 bench mirror — Go. Same DP, same checksum.
package main

import "fmt"

const N = 300000

func main() {
	least := make([]int64, N+1)
	for i := int64(1); i <= N; i++ {
		best := i
		for j := int64(1); j*j <= i; j++ {
			cand := least[i-j*j] + 1
			if cand < best {
				best = cand
			}
		}
		least[i] = best
	}
	var sum int64
	for k := 0; k <= N; k++ {
		sum = (sum*31 + least[k]) % 1000000007
	}
	fmt.Println((sum*10 + least[N]) % 1000000007)
}
