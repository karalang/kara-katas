// LeetCode #1497: Check If Array Pairs Are Divisible by k -- the bench in
// Go, mirroring can_arrange.kara: each value's remainder by k counted.
package main

import "fmt"

func canArrange(arr []int32, k int32) bool {
	count := make([]int64, k)
	for _, x := range arr {
		count[(x%k+k)%k]++
	}
	if count[0]%2 != 0 {
		return false
	}
	for r := int32(1); r < k; r++ {
		if count[r] != count[k-r] {
			return false
		}
	}
	return true
}

func main() {
	var seed int64 = 1497
	arr := make([]int32, 0, 100000)
	for i := 0; i < 50000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		x := seed/65536*30011%2000000001 - 1000000000
		arr = append(arr, int32(x), int32(1000*(seed%7)-x))
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		k := 1 + (check+call)%100000
		if call%2 == 0 {
			k = 1000
		}
		at := (check*7 + call) % 100000
		if call%4 < 2 {
			arr[at] += 1000
		} else {
			arr[at] -= 1000
		}
		yes := canArrange(arr, int32(k))
		add := int64(1)
		if yes {
			add = 2
		}
		check = (check*31 + k + add) % 1000000007
	}
	fmt.Printf("1000 calls over 100000 values: checksum %d\n", check)
}
