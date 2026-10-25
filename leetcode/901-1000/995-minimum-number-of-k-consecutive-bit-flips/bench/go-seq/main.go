// Benchmark: LeetCode #995 Minimum Number of K Consecutive Bit Flips --
// the ★ arm, the greedy with a running parity, on random arrays of
// 100000 bits, LeetCode's largest. Mirrors min_k_bit_flips.kara, .c, .rs
// and .py.
package main

import "fmt"

func minKBitFlips(nums []int64, k int) int64 {
	n := len(nums)
	ends := make([]bool, n+1)
	flipped := false
	var flips int64
	for i := 0; i < n; i++ {
		if ends[i] {
			flipped = !flipped
		}
		if (nums[i] == 1) == flipped {
			if i+k > n {
				return -1
			}
			flips++
			flipped = !flipped
			ends[i+k] = true
		}
	}
	return flips
}

var seed int64 = 995

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 50
	// ten arrays of random bits and ten of ones put through random flips
	// of 1 to 100 bits, which can be made all ones again
	arrays := make([][]int64, 20)
	ks := make([]int, 20)
	for a := 0; a < 20; a++ {
		nums := make([]int64, 100000)
		if a%2 == 0 {
			for i := range nums {
				nums[i] = nextRandom() % 2
			}
			ks[a] = 1 + int(nextRandom()%100)
		} else {
			k := 1 + int(nextRandom()%100)
			for i := range nums {
				nums[i] = 1
			}
			for i := 0; i < 100000-k+1; i++ {
				if nextRandom()%4 == 0 {
					for j := i; j < i+k; j++ {
						nums[j] = 1 - nums[j]
					}
				}
			}
			ks[a] = k
		}
		arrays[a] = nums
	}
	var stuck, total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			a := (r + i) % 20
			got := minKBitFlips(arrays[a], ks[a])
			if got < 0 {
				stuck++
			} else {
				total += got
			}
			check = (check*31 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 arrays of 100000 bits: %d impossible, %d flips, checksum %d\n", rounds, stuck, total, check)
}
