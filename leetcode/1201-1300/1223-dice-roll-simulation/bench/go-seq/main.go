// LeetCode #1223 bench, Go mirror of the Kāra ★ arm: count the sequences
// by their last face and run length, for 50 random sets of limits at
// n = 5000; checksum of the answers.
package main

import "fmt"

var seed int64 = 1223

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func dieSimulator(n int64, rollMax []int64) int64 {
	const modulus int64 = 1_000_000_007
	count := make([][]int64, 6)
	for f := range count {
		count[f] = make([]int64, 15)
		count[f][0] = 1
	}
	for step := int64(1); step < n; step++ {
		next := make([][]int64, 6)
		for f := range next {
			next[f] = make([]int64, 15)
		}
		for f := 0; f < 6; f++ {
			for r := int64(0); r < rollMax[f]; r++ {
				c := count[f][r]
				if c == 0 {
					continue
				}
				for g := 0; g < 6; g++ {
					if g != f {
						next[g][0] = (next[g][0] + c) % modulus
					} else if r+1 < rollMax[f] {
						next[f][r+1] = (next[f][r+1] + c) % modulus
					}
				}
			}
		}
		count = next
	}
	var total int64
	for f := 0; f < 6; f++ {
		for r := 0; r < 15; r++ {
			total = (total + count[f][r]) % modulus
		}
	}
	return total
}

func main() {
	var check int64
	for t := 0; t < 50; t++ {
		rollMax := make([]int64, 6)
		for f := range rollMax {
			rollMax[f] = nextRandom()%15 + 1
		}
		check = (check*131 + dieSimulator(5000, rollMax)) % 1000000007
	}
	fmt.Printf("50 sets of limits at n = 5000: checksum %d\n", check)
}
