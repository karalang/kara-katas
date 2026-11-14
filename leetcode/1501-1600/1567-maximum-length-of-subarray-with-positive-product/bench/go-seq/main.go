// LeetCode #1567: Maximum Length of Subarray With Positive Product --
// bench: the ★ arm over 20 arrays of 200000 values, built once, each
// value 0 one time in 5000 and otherwise of 1 to 1000, negative one time in
// three; 20 passes, each first flipping the sign of one value of every
// array.
package main

import "fmt"

func getMaxLen(nums []int64) int64 {
	var positive, negative, best int64
	for _, x := range nums {
		if x > 0 {
			positive++
			if negative > 0 {
				negative++
			} else {
				negative = 0
			}
		} else if x < 0 {
			wasPositive := positive
			if negative > 0 {
				positive = negative + 1
			} else {
				positive = 0
			}
			negative = wasPositive + 1
		} else {
			positive = 0
			negative = 0
		}
		if positive > best {
			best = positive
		}
	}
	return best
}

var seed int64 = 1567

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 200000
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			size := nextRandom()%1000 + 1
			kind := nextRandom()
			var v int64
			if kind%5000 == 0 {
				v = 0
			} else if kind%3 == 0 {
				v = -size
			} else {
				v = size
			}
			nums = append(nums, v)
		}
		arrays = append(arrays, nums)
	}
	var check, total int64
	for p := int64(0); p < 20; p++ {
		for a := range arrays {
			at := (p*7919 + int64(a)*104729) % n
			arrays[a][at] = -arrays[a][at]
			length := getMaxLen(arrays[a])
			total += length
			check = mix(check, length)
		}
	}
	fmt.Printf("20 passes over 20 arrays of 200000 values: lengths sum %d, checksum %d\n", total, check)
}
