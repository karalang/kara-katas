// LeetCode 798 — Smallest Rotation with Highest Score: the bench, in Go.
// Mirrors best_rotation.kara: a difference array over the rotations.
package main

import "fmt"

func bestRotation(nums []int64) int64 {
	n := int64(len(nums))
	change := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		first := (i + 1) % n
		last := (i - nums[i] + n) % n
		change[first]++
		change[last+1]--
		if first > last {
			change[0]++
			change[n]--
		}
	}
	var best, score int64
	var bestScore int64 = -1
	for k := int64(0); k < n; k++ {
		score += change[k]
		if score > bestScore {
			bestScore = score
			best = k
		}
	}
	return best
}

var seed int64 = 798

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 100000
	arrays := make([][]int64, 0, 16)
	for a := 0; a < 16; a++ {
		hi := nextRandom()
		top := 1 + (hi*32768+nextRandom())%n
		nums := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			h := nextRandom()
			nums = append(nums, (h*32768+nextRandom())%top)
		}
		arrays = append(arrays, nums)
	}
	var rounds int64 = 4000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		k := bestRotation(arrays[r%16])
		total += k
		check = (check*131 + k) % 1000000007
	}
	fmt.Printf("%d rounds of %d numbers: rotations adding up to %d, checksum %d\n", rounds, n, total, check)
}
