// LeetCode #2369: Check if There is a Valid Partition For The Array -- the
// bench, the ★ arm in Go: good[i] says whether the first i values split
// into valid blocks, from the last block before i and the values before
// it.
package main

import "fmt"

func validPartition(nums []int64) bool {
	n := len(nums)
	good := make([]bool, n+1)
	good[0] = true
	for i := 2; i <= n; i++ {
		a := nums[i-1]
		b := nums[i-2]
		if a == b && good[i-2] {
			good[i] = true
		}
		if i >= 3 && good[i-3] {
			c := nums[i-3]
			if (a == b && b == c) || (b == c+1 && a == b+1) {
				good[i] = true
			}
		}
	}
	return good[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// array a: about 10^5 values in random blocks of two or three equal
	// values or three rising, the values up to 4^(a + 1); when a is odd, one
	// value near the end then raised by one
	seed := int64(2369)
	arrays := make([][]int64, 0, 10)
	top := int64(4)
	for a := 0; a < 10; a++ {
		nums := []int64{}
		for len(nums) < 100000 {
			kind := nextRandom(&seed) % 3
			hi := nextRandom(&seed)
			v := 1 + (hi*32768+nextRandom(&seed))%top
			if kind == 0 {
				nums = append(nums, v, v)
			} else if kind == 1 {
				nums = append(nums, v, v, v)
			} else {
				nums = append(nums, v, v+1, v+2)
			}
		}
		if a%2 == 1 {
			at := len(nums) - 1 - int(nextRandom(&seed)%100)
			nums[at]++
		}
		arrays = append(arrays, nums)
		top *= 4
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for a := 0; a < 10; a++ {
			valid := int64(0)
			if validPartition(arrays[a]) {
				valid = int64(a) + 1
			}
			check = (check*31 + valid + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 arrays of about 10^5 values: checksum %d\n", check)
}
