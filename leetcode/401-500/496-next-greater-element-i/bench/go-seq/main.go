// Benchmark for #496: Go mirror of the ★ arm (a stack and a map); see
// ../next_greater_element.kara.
package main

import "fmt"

func nextGreaterElement(nums1, nums2 []int64) []int64 {
	next := map[int64]int64{}
	waiting := []int64{}
	for _, x := range nums2 {
		for len(waiting) > 0 {
			top := waiting[len(waiting)-1]
			if top >= x {
				break
			}
			next[top] = x
			waiting = waiting[:len(waiting)-1]
		}
		waiting = append(waiting, x)
	}
	out := []int64{}
	for _, x := range nums1 {
		if g, ok := next[x]; ok {
			out = append(out, g)
		} else {
			out = append(out, -1)
		}
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 10,000 cases, built once: nums2 is 1,000 distinct numbers from 0
	// to 10,000 (the problem's most), drawn by shuffling the front of a
	// pool of all of them, and nums1 is every other one of them from the
	// end. Then each case is solved once.
	cases := 10000
	var seed int64 = 496
	pool := make([]int64, 10001)
	for x := range pool {
		pool[x] = int64(x)
	}
	all1 := [][]int64{}
	all2 := [][]int64{}
	for c := 0; c < cases; c++ {
		for i := 0; i < 1000; i++ {
			j := i + int(nextRandom(&seed)%int64(10001-i))
			pool[i], pool[j] = pool[j], pool[i]
		}
		nums2 := make([]int64, 1000)
		copy(nums2, pool[:1000])
		nums1 := []int64{}
		for k := 999; k >= 0; k -= 2 {
			nums1 = append(nums1, nums2[k])
		}
		all1 = append(all1, nums1)
		all2 = append(all2, nums2)
	}
	found := 0
	var checksum int64
	for c := 0; c < cases; c++ {
		for _, a := range nextGreaterElement(all1[c], all2[c]) {
			if a >= 0 {
				found++
			}
			checksum = (checksum*31 + a + 2) % 1000000007
		}
	}
	fmt.Printf("%d cases of 1000 and 500: %d with a greater number, checksum %d\n", cases, found, checksum)
}
