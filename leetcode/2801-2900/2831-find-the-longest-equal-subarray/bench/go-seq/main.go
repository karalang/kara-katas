// LeetCode #2831: Find the Longest Equal Subarray -- the bench, mirrored
// from equal.kara: positions per value, then two pointers over each list.
package main

import "fmt"

func longestEqualSubarray(nums []int64, k int64) int64 {
	n := len(nums)
	places := make([][]int64, n+1)
	for i := 0; i < n; i++ {
		places[nums[i]] = append(places[nums[i]], int64(i))
	}
	var best int64
	for _, pos := range places {
		l := 0
		for r := 0; r < len(pos); r++ {
			for pos[r]-pos[l]-int64(r-l) > k {
				l++
			}
			if int64(r-l+1) > best {
				best = int64(r - l + 1)
			}
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type array struct {
	nums []int64
	k    int64
}

func main() {
	const count, rounds, n = 20, 20, 100000
	seed := int64(2831)
	arrays := make([]array, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = nextRandom(&seed)%1000 + 1
		}
		arrays = append(arrays, array{nums, nextRandom(&seed) % 1001})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, a := range arrays {
			x := longestEqualSubarray(a.nums, a.k)
			total += x
			check = (check*31 + x + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: lengths total %d, checksum %d\n", count, n, rounds, total, check)
}
