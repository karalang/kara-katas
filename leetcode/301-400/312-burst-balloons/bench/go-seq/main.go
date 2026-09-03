// Benchmark workload for LeetCode #312 - Burst Balloons.
//
// Mirror of burst.kara: same interval DP, same flat table reused across
// passes, same serial dependency between passes, same masked sink. Kept
// algorithm-for-algorithm so the cross-language comparison is honest.

package main

import "fmt"

func solve(a []int64, w int64, dp []int64) int64 {
	for length := int64(2); length < w; length++ {
		for i := int64(0); i < w-length; i++ {
			j := i + length
			ai := a[i]
			aj := a[j]
			base := i * w
			var best int64 = 0
			for k := i + 1; k < j; k++ {
				coins := dp[base+k] + dp[k*w+j] + ai*a[k]*aj
				if coins > best {
					best = coins
				}
			}
			dp[base+j] = best
		}
	}
	return dp[w-1]
}

func main() {
	const n int64 = 300
	const w int64 = n + 2
	const passes int64 = 88

	a := make([]int64, 0, w)
	a = append(a, 1)
	var state int64 = 987654321
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		a = append(a, 1+state%50)
	}
	a = append(a, 1)

	dp := make([]int64, w*w)

	var checksum int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := 1 + checksum%n
		a[idx] = 1 + (a[idx]+checksum)%50
		total := solve(a, w, dp)
		checksum = (checksum + total) & 1073741823
	}

	fmt.Printf("checksum %d\n", checksum)
}
