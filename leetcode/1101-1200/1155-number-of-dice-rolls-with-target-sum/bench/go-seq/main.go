// LeetCode #1155 bench -- mirrors num_rolls_to_target.kara: the same 64
// problems, the same passes, the ★ arm's rolling counts.
package main

import "fmt"

func numRollsToTarget(n, k, target int64) int64 {
	const modulus = 1000000007
	ways := make([]int64, target+1)
	ways[0] = 1
	for d := int64(0); d < n; d++ {
		next := make([]int64, target+1)
		for s := int64(0); s < target+1; s++ {
			if ways[s] != 0 {
				for face := int64(1); face < k+1; face++ {
					if s+face > target {
						break
					}
					next[s+face] = (next[s+face] + ways[s]) % modulus
				}
			}
		}
		ways = next
	}
	return ways[target]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	passes := int64(250)
	seed := int64(1155)
	problems := make([][3]int64, 0, 64)
	for i := 0; i < 64; i++ {
		n := 1 + nextRandom(&seed)%30
		k := 1 + nextRandom(&seed)%30
		most := n * k
		if most > 1000 {
			most = 1000
		}
		problems = append(problems, [3]int64{n, k, n + nextRandom(&seed)%(most-n+1)})
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, q := range problems {
			check = (check*31 + numRollsToTarget(q[0], q[1], q[2]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 64 problems: checksum %d\n", passes, check)
}
