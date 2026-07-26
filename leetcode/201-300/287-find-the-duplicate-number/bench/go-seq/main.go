// Benchmark harness for LeetCode #287 — Find the Duplicate Number.
// Mirrors find_duplicate.kara algorithm-for-algorithm.

package main

import "fmt"

func findDuplicate(nums []int64) int64 {
	slow := nums[0]
	fast := nums[0]
	slow = nums[slow]
	fast = nums[nums[fast]]
	for slow != fast {
		slow = nums[slow]
		fast = nums[nums[fast]]
	}
	finder := nums[0]
	for finder != slow {
		finder = nums[finder]
		slow = nums[slow]
	}
	return finder
}

func main() {
	const np int64 = 4
	const n int64 = 200000
	const iters int64 = 80

	arrays := make([][]int64, 0, np)
	for p := int64(0); p < np; p++ {
		order := make([]int64, 0, n)
		for v := int64(1); v <= n; v++ {
			order = append(order, v)
		}
		x := p + 12345
		for k := n - 1; k > 0; k-- {
			x = (x*1103515245 + 12345) % 2147483648
			j := (x / 65536) % (k + 1)
			order[k], order[j] = order[j], order[k]
		}

		arr := make([]int64, 0, n+1)
		for z := int64(0); z <= n; z++ {
			arr = append(arr, 0)
		}
		for t := int64(0); t < n; t++ {
			nxt := (t + 1) % n
			arr[order[t]] = order[nxt]
		}
		arr[0] = order[p*37]
		arrays = append(arrays, arr)
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		idx := (it * 3) % np
		sink = (sink*31 + findDuplicate(arrays[idx])) % 1000000007
	}
	fmt.Println(sink)
}
