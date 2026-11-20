// LeetCode #1692: Count Ways to Distribute Candies -- the bench's Go mirror:
// the ★ arm on 200 problems of 1000 candies, each with a random number of
// bags up to 1000, all drawn first, each answered 8 times.
package main

import "fmt"

func waysToDistribute(n, k int32) int32 {
	const modulus = 1000000007
	ways := make([]int64, k+1)
	ways[0] = 1
	for i := int64(1); i <= int64(n); i++ {
		for j := min(i, int64(k)); j >= 1; j-- {
			ways[j] = (j*ways[j] + ways[j-1]) % modulus
		}
		ways[0] = 0
	}
	return int32(ways[k])
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1692

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 200, 8, 1000
	bags := make([]int32, count)
	for i := range bags {
		bags[i] = int32(nextRandom()%n + 1)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, k := range bags {
			answer := int64(waysToDistribute(n, k))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d candies, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
