// Benchmark: LeetCode #941 Valid Mountain Array -- the ★ arm, a walk up
// and a walk down, on 100 arrays of 10000 values, LeetCode's longest, in
// 200 rounds. Mirrors valid_mountain_array.kara, .c, .rs and .py.
package main

import "fmt"

func validMountainArray(arr []int64) bool {
	n := len(arr)
	i := 0
	for i+1 < n && arr[i] < arr[i+1] {
		i++
	}
	if i == 0 || i == n-1 {
		return false
	}
	for i+1 < n && arr[i] > arr[i+1] {
		i++
	}
	return i == n-1
}

var seed int64 = 941

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 200, 100
	arrays := make([][]int64, 0, count)
	for a := 0; a < count; a++ {
		top := 1 + nextRandom()%9998
		var least int64
		if top >= 10000-top {
			least = 2*top - 9999
		}
		arr := make([]int64, 10000)
		for i := int64(0); i < 10000; i++ {
			if i <= top {
				arr[i] = i - least
			} else {
				arr[i] = 2*top - i - least
			}
		}
		if a%2 == 1 {
			hi := nextRandom()
			j := (hi*32768 + nextRandom()) % 10000
			arr[j] = nextRandom() % 10001
		}
		arrays = append(arrays, arr)
	}
	var mountains, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			c := (r + i) % count
			if validMountainArray(arrays[c]) {
				mountains++
				check = (check*1000003 + int64(c) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d arrays of 10000 values: %d mountains, checksum %d\n", rounds, count, mountains, check)
}
