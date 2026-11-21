// LeetCode #2470: Number of Subarrays With LCM Equal to K -- the bench,
// the ★ arm in Go: from each start the running LCM, the walk stopped once
// it no longer divides `k`, the gcd recursive as in Kāra.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func subarrayLCM(nums []int64, k int64) int64 {
	n := len(nums)
	var count int64
	for start := 0; start < n; start++ {
		var lcm int64 = 1
		for end := start; end < n; end++ {
			lcm = lcm / gcd(lcm, nums[end]) * nums[end]
			if k%lcm != 0 {
				break
			}
			if lcm == k {
				count++
			}
		}
	}
	return count
}

var seed int64 = 2470

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 10 lists of 1000 numbers built once, each a random divisor of 720
	// but one in 50 any number from 1 to 1000; then 90 passes, each
	// setting one number of every list from the checksum so far, then
	// answering it with `k` 720 and folding the count plus the pass into
	// the checksum
	divisors := []int64{}
	for d := int64(1); d <= 720; d++ {
		if 720%d == 0 {
			divisors = append(divisors, d)
		}
	}
	nd := int64(len(divisors))
	lists := make([][]int64, 10)
	for a := range lists {
		lists[a] = make([]int64, 1000)
		for i := range lists[a] {
			if nextRandom()%50 == 0 {
				lists[a][i] = 1 + nextRandom()%1000
			} else {
				lists[a][i] = divisors[nextRandom()%nd]
			}
		}
	}
	var check int64
	for p := int64(0); p < 90; p++ {
		for a := range lists {
			lists[a][(check+int64(a))%1000] = divisors[check%nd]
			check = (check*31 + subarrayLCM(lists[a], 720) + p) % 1000000007
		}
	}
	fmt.Printf("90 passes over 10 lists of 1000: checksum %d\n", check)
}
