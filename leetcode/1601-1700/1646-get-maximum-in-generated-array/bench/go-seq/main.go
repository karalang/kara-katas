// LeetCode #1646: Get Maximum in Generated Array -- the bench's Go mirror:
// the ★ arm on 4000000 random n from 0 to 100, all drawn first.
package main

import "fmt"

func getMaximumGenerated(n int32) int32 {
	if n == 0 {
		return 0
	}
	nums := make([]int32, n+1)
	nums[1] = 1
	best := int32(1)
	for i := int32(2); i <= n; i++ {
		if i%2 == 0 {
			nums[i] = nums[i/2]
		} else {
			nums[i] = nums[i/2] + nums[i/2+1]
		}
		if nums[i] > best {
			best = nums[i]
		}
	}
	return best
}

var seed int64 = 1646

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const cases = 4000000
	ns := make([]int32, cases)
	for c := range ns {
		ns[c] = int32(nextRandom() % 101)
	}
	var check, total int64
	for _, n := range ns {
		found := int64(getMaximumGenerated(n))
		total += found
		check = (check*31 + found + 1) % 1000000007
	}
	fmt.Printf("%d random n up to 100: maxima sum to %d, checksum %d\n", cases, total, check)
}
