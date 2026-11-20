// LeetCode #1681: Minimum Incompatibility -- the bench's Go mirror: the ★
// arm on 300 arrays of 16 values from 1 to 16, each with a random k that
// divides 16, all drawn first, each answered 4 times.

package main

import (
	"fmt"
	"math"
	"math/bits"
)

func minimumIncompatibility(nums []int32, k int32) int32 {
	n := len(nums)
	size := n / int(k)
	full := (1 << n) - 1
	cost := make([]int32, 1<<n)
	for s := 0; s <= full; s++ {
		cost[s] = -1
		if bits.OnesCount(uint(s)) != size {
			continue
		}
		var seen int64
		lo, hi := int32(math.MaxInt32), int32(math.MinInt32)
		ok := true
		for i := 0; i < n; i++ {
			if s>>i&1 == 1 {
				bit := int64(1) << nums[i]
				if seen&bit != 0 {
					ok = false
					break
				}
				seen |= bit
				lo = min(lo, nums[i])
				hi = max(hi, nums[i])
			}
		}
		if ok {
			cost[s] = hi - lo
		}
	}
	const unreached = int32(math.MaxInt32)
	best := make([]int32, 1<<n)
	for m := range best {
		best[m] = unreached
	}
	best[0] = 0
	for m := 0; m < full; m++ {
		if best[m] == unreached || bits.OnesCount(uint(m))%size != 0 {
			continue
		}
		free := full ^ m
		lowest := free & -free
		for s := free; s > 0; s = (s - 1) & free {
			if s&lowest != 0 && cost[s] >= 0 {
				best[m|s] = min(best[m|s], best[m]+cost[s])
			}
		}
	}
	if best[full] == unreached {
		return -1
	}
	return best[full]
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1681

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 300
	const n = 16
	const rounds = 4
	ks := []int32{1, 2, 4, 8, 16}
	type problem struct {
		nums []int32
		k    int32
	}
	cases := make([]problem, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(nextRandom()%n + 1)
		}
		k := ks[nextRandom()%5]
		cases = append(cases, problem{nums, k})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			answer := int64(minimumIncompatibility(c.nums, c.k))
			total += answer
			check = (check*31 + answer + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers sum to %d, checksum %d\n", arrays, n, rounds, total, check)
}
