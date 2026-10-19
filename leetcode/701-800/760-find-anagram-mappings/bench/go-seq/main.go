// LeetCode 760 — Find Anagram Mappings: benchmark, the ★ arm in Go.
package main

import "fmt"

func anagramMappings(nums1, nums2 []int64) []int64 {
	positions := map[int64][]int64{}
	for j, x := range nums2 {
		positions[x] = append(positions[x], int64(j))
	}
	used := map[int64]int{}
	mapping := []int64{}
	for _, x := range nums1 {
		k := used[x]
		mapping = append(mapping, positions[x][k])
		used[x] = k + 1
	}
	return mapping
}

var seed int64 = 760

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 100000
	fixed := 0
	check := int64(0)
	for r := 0; r < rounds; r++ {
		nums1 := make([]int64, 100)
		for i := range nums1 {
			nums1[i] = nextRandom() % 50
		}
		nums2 := make([]int64, 100)
		copy(nums2, nums1)
		for i := 0; i < 100; i++ {
			j := i + int(nextRandom()%int64(100-i))
			nums2[i], nums2[j] = nums2[j], nums2[i]
		}
		mapping := anagramMappings(nums1, nums2)
		for i := 0; i < 100; i++ {
			if mapping[i] == int64(i) {
				fixed++
			}
			check = (check*31 + mapping[i]) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 100 values: %d mapped to their own index, checksum %d\n", rounds, fixed, check)
}
