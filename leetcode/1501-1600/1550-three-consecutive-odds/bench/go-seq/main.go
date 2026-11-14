// LeetCode #1550: Three Consecutive Odds -- bench: the ★ arm (the run of
// odd values) over 1000 arrays of 1 to 1000 values, each with its own
// chance of an odd value, built once, each asked 2000 times with one value
// raised by one before every ask, so no ask repeats the last. Go mirror
// of three_odds.kara.
package main

import "fmt"

func threeConsecutiveOdds(arr []int64) bool {
	run := 0
	for _, x := range arr {
		if x%2 == 1 {
			run++
			if run == 3 {
				return true
			}
		} else {
			run = 0
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1550)
	arrays := [][]int64{}
	for g := 0; g < 1000; g++ {
		length := (nextRandom(&seed)*32768+nextRandom(&seed))%1000 + 1
		odds := nextRandom(&seed) % 101
		arr := []int64{}
		for i := int64(0); i < length; i++ {
			odd := nextRandom(&seed)%100 < odds
			half := nextRandom(&seed) % 500
			if odd {
				arr = append(arr, 2*half+1)
			} else {
				arr = append(arr, 2*half+2)
			}
		}
		arrays = append(arrays, arr)
	}
	yes, check := int64(0), int64(0)
	for pass := int64(0); pass < 2000; pass++ {
		for g := range arrays {
			at := (pass*7 + int64(g)) % int64(len(arrays[g]))
			arrays[g][at]++
			if threeConsecutiveOdds(arrays[g]) {
				yes++
				check = (check*31 + pass + int64(g) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("2000 passes over 1000 arrays of up to 1000 values: %d true, checksum %d\n", yes, check)
}
