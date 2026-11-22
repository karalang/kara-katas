// LeetCode #2845: Count of Interesting Subarrays -- the bench, mirrored
// from interesting.kara: a map from each prefix count mod modulo to how
// often it has come up, read before each new prefix is added.
package main

import "fmt"

func countInterestingSubarrays(nums []int64, modulo, k int64) int64 {
	seen := map[int64]int64{0: 1}
	var prefix, count int64
	for _, x := range nums {
		if x%modulo == k {
			prefix = (prefix + 1) % modulo
		}
		want := (prefix - k + modulo) % modulo
		count += seen[want]
		seen[prefix]++
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds = 10, 100000, 20
	seed := int64(2845)
	type caseT struct {
		nums      []int64
		modulo, k int64
	}
	cases := make([]caseT, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			hi := nextRandom(&seed)
			nums[i] = (hi*32768+nextRandom(&seed))%1000000000 + 1
		}
		top := int64(100000)
		if c%2 == 0 {
			top = 10
		}
		modulo := nextRandom(&seed)%top + 1
		k := nextRandom(&seed) % modulo
		cases = append(cases, caseT{nums, modulo, k})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			got := countInterestingSubarrays(cs.nums, cs.modulo, cs.k)
			total += got
			check = (check*31 + got%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: %d subarrays, checksum %d\n", count, n, rounds, total, check)
}
