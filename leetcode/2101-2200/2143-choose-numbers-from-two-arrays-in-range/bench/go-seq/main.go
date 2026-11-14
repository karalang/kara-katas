// LeetCode #2143: Choose Numbers From Two Arrays in Range -- the
// benchmark, the same algorithm as choose.kara.
package main

import "fmt"

func countSubranges(nums1, nums2 []int64) int64 {
	const modulus = 1000000007
	low, high := int64(0), int64(0)
	for i := range nums1 {
		low += nums2[i]
		high += nums1[i]
	}
	width := low + high + 1
	ways := make([]int64, width)
	balanced := int64(0)
	for i := range nums1 {
		ways[low]++
		next := make([]int64, width)
		a, b := nums1[i], nums2[i]
		for d := int64(0); d < width; d++ {
			if ways[d] > 0 {
				next[d+a] = (next[d+a] + ways[d]) % modulus
				next[d-b] = (next[d-b] + ways[d]) % modulus
			}
		}
		ways = next
		balanced = (balanced + ways[low]) % modulus
	}
	return balanced
}

var seed int64 = 2143

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	firsts := make([][]int64, 4)
	seconds := make([][]int64, 4)
	for p := 0; p < 4; p++ {
		firsts[p] = make([]int64, 100)
		seconds[p] = make([]int64, 100)
		for i := range firsts[p] {
			firsts[p][i] = nextRandom() % 101
		}
		for i := range seconds[p] {
			seconds[p][i] = nextRandom() % 101
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 50; round++ {
		for p := 0; p < 4; p++ {
			at := nextRandom() % 100
			firsts[p][at] = nextRandom() % 101
			seconds[p][at] = nextRandom() % 101
			ways := countSubranges(firsts[p], seconds[p])
			total += ways
			check = (check*31 + ways + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d ranges in all, checksum %d\n", total, check)
}
