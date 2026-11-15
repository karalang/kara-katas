// LeetCode #2179: Count Good Triplets in an Array -- the benchmark's Go
// mirror of triplets.kara, over slices.
package main

import "fmt"

func goodTriplets(nums1, nums2 []int64) int64 {
	n := int64(len(nums1))
	place := make([]int64, n)
	for i := int64(0); i < n; i++ {
		place[nums2[i]] = i
	}
	tree := make([]int64, n+1)
	var total int64
	for i := int64(0); i < n; i++ {
		p := place[nums1[i]]
		var smaller int64
		j := p
		for j > 0 {
			smaller += tree[j]
			j -= j & -j
		}
		larger := (n - 1 - p) - (i - smaller)
		total += smaller * larger
		j = p + 1
		for j <= n {
			tree[j]++
			j += j & -j
		}
	}
	return total
}

var seed int64 = 2179

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func shuffled(n int64) []int64 {
	perm := make([]int64, n)
	for i := int64(0); i < n; i++ {
		perm[i] = i
	}
	for i := n - 1; i > 0; i-- {
		a := nextRandom()
		b := nextRandom()
		j := (a*32768 + b) % (i + 1)
		perm[i], perm[j] = perm[j], perm[i]
	}
	return perm
}

func main() {
	var n int64 = 100000
	first := shuffled(n)
	second := shuffled(n)
	var check int64
	for r := 0; r < 40; r++ {
		a := nextRandom()
		b := nextRandom()
		offset := (a*32768 + b) % n
		rotated := make([]int64, n)
		for i := int64(0); i < n; i++ {
			rotated[i] = second[(i+offset)%n]
		}
		found := goodTriplets(first, rotated)
		check = (check*31 + found%1000000007) % 1000000007
	}
	fmt.Printf("40 solves: checksum %d\n", check)
}
