// LeetCode #2295: Replace Elements in an Array -- the bench, the ★ arm in
// Go. A map from each number to its index finds the one to replace at
// once; the replacement takes over the index.
package main

import "fmt"

func arrayChange(nums []int64, operations [][2]int64) []int64 {
	out := append([]int64(nil), nums...)
	at := make(map[int64]int, len(out))
	for i, x := range out {
		at[x] = i
	}
	for _, op := range operations {
		i := at[op[0]]
		delete(at, op[0])
		out[i] = op[1]
		at[op[1]] = i
	}
	return out
}

var seed int64 = 2295

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return (hi*32768+nextRandom())%1000000 + 1
}

type kase struct {
	nums []int64
	ops  [][2]int64
}

func main() {
	var cases []kase
	for c := 0; c < 10; c++ {
		n := 100000
		present := make([]bool, 1000001)
		var nums []int64
		for len(nums) < n {
			x := wide()
			if !present[x] {
				present[x] = true
				nums = append(nums, x)
			}
		}
		now := append([]int64(nil), nums...)
		var ops [][2]int64
		for o := 0; o < 100000; o++ {
			i := nextRandom() % int64(n)
			to := wide()
			for present[to] {
				to = to%1000000 + 1
			}
			present[now[i]] = false
			present[to] = true
			ops = append(ops, [2]int64{now[i], to})
			now[i] = to
		}
		cases = append(cases, kase{nums, ops})
	}
	var check int64
	for pass := 0; pass < 3; pass++ {
		for _, k := range cases {
			for _, x := range arrayChange(k.nums, k.ops) {
				check = (check*31 + x) % 1000000007
			}
		}
	}
	fmt.Printf("3 passes over 10 arrays of 10^5 with 10^5 operations: checksum %d\n", check)
}
