// LeetCode #1508: Range Sum of Sorted Subarray Sums -- the bench: 40 arrays
// of 1000 numbers built once, then 25 ranges of places asked of each, by
// the ★ arm.
package main

import "fmt"

const mod = 1000000007

func atMost(prefix, twice []int64, bound int64) (int64, int64) {
	n := len(prefix) - 1
	var count, total int64
	i := 0
	for j := 1; j <= n; j++ {
		for prefix[j]-prefix[i] > bound {
			i++
		}
		w := int64(j - i)
		count += w
		total += w*prefix[j] - (twice[j] - twice[i])
	}
	return count, total
}

func smallest(prefix, twice []int64, k int64) int64 {
	if k == 0 {
		return 0
	}
	lo, hi := int64(1), prefix[len(prefix)-1]
	for lo < hi {
		mid := (lo + hi) / 2
		if c, _ := atMost(prefix, twice, mid); c >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	count, total := atMost(prefix, twice, lo)
	return total - (count-k)*lo
}

func rangeSum(nums []int64, n int, left, right int64) int64 {
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + nums[i]
	}
	twice := make([]int64, n+1)
	for i := 0; i < n; i++ {
		twice[i+1] = twice[i] + prefix[i]
	}
	return (smallest(prefix, twice, right) - smallest(prefix, twice, left-1)) % mod
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1508)
	arrays := make([][]int64, 40)
	for a := range arrays {
		arrays[a] = make([]int64, 1000)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom(&seed)%100 + 1
		}
	}
	total := int64(1000 * 1001 / 2)
	var check int64
	for r := 0; r < 25; r++ {
		for _, nums := range arrays {
			a := nextRandom(&seed)%total + 1
			b := nextRandom(&seed)%total + 1
			lo, hi := a, b
			if b < a {
				lo, hi = b, a
			}
			check = (check*31 + rangeSum(nums, 1000, lo, hi) + 1) % 1000000007
		}
	}
	fmt.Printf("1000 ranges over 40 arrays of 1000 numbers: checksum %d\n", check)
}
