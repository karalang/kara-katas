// Benchmark for #548: Go mirror of the ★ arm (a set of left sums per
// middle cut); see ../split_array_with_equal_sum.kara.
package main

import "fmt"

func splitArray(nums []int64) bool {
	n := len(nums)
	if n < 7 {
		return false
	}
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + nums[i]
	}
	for j := 3; j < n-3; j++ {
		sums := map[int64]struct{}{}
		for i := 1; i < j-1; i++ {
			if prefix[i] == prefix[j]-prefix[i+1] {
				sums[prefix[i]] = struct{}{}
			}
		}
		for k := j + 2; k < n-1; k++ {
			third := prefix[k] - prefix[j+1]
			if third == prefix[n]-prefix[k+1] {
				if _, ok := sums[third]; ok {
					return true
				}
			}
		}
	}
	return false
}

var seed int64 = 548

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, n := 10, 2000
	all := make([][]int64, count)
	for g := 0; g < count; g++ {
		spread := int64(1 + g%5*25)
		a := make([]int64, n)
		for i := range a {
			a[i] = nextRandom()%(2*spread+1) - spread
		}
		all[g] = a
	}
	var yes, checksum int64
	for round := 0; round < 20; round++ {
		for g := 0; g < count; g++ {
			i := (round*31 + g*7) % n
			all[g][i] = -all[g][i]
			var bit int64
			if splitArray(all[g]) {
				bit = 1
			}
			yes += bit
			checksum = (checksum*31 + bit + 7*int64(g)) % 1000000007
		}
	}
	fmt.Printf("%d arrays, 20 rounds each: %d can be split, checksum %d\n", count, yes, checksum)
}
