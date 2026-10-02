// Benchmark workload for LeetCode #325 — Go mirror of max_sub_len.kara.
//
// Go's built-in map (its own runtime hash, not SipHash). A fresh map per
// call, a comma-ok lookup, and an insert guarded by a second lookup for the
// first-occurrence rule, which is how Go spells `entry().or_insert()`.
package main

import "fmt"

const LEN = 200000
const PUNCHES = 60
const MODULUS = 1073741789

func maxSubLen(nums []int64, k int64) int64 {
	first := map[int64]int64{0: -1}
	var p, best int64
	for i := int64(0); i < int64(len(nums)); i++ {
		p += nums[i]
		if j, ok := first[p-k]; ok && i-j > best {
			best = i - j
		}
		if _, ok := first[p]; !ok {
			first[p] = i
		}
	}
	return best
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(325)
	ranges := []int64{1, 100, 10000}
	arrays := make([][]int64, 0, 3)
	for _, r := range ranges {
		a := make([]int64, 0)
		for i := 0; i < LEN; i++ {
			a = append(a, next(&seed)%(2*r+1)-r)
		}
		arrays = append(arrays, a)
	}

	var sink int64
	for punch := int64(0); punch < PUNCHES; punch++ {
		t := punch % 3
		r := ranges[t]
		hi := next(&seed)
		pos := (hi*32768 + next(&seed)) % LEN
		arrays[t][pos] = next(&seed)%(2*r+1) - r
		k := (next(&seed)%41 - 20) * r / 4
		l := maxSubLen(arrays[t], k)
		sink = (sink*31 + l + 1) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
