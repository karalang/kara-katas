// LeetCode #2439: Minimize Maximum of Array -- the bench, the ★ arm: the
// largest ceiling average of any prefix, in one pass.
package main

import "fmt"

func minimizeArrayValue(nums []int64) int64 {
	var sum, answer int64
	for i := range nums {
		sum += nums[i]
		k := int64(i)
		if a := (sum + k) / (k + 1); a > answer {
			answer = a
		}
	}
	return answer
}

var seed int64 = 2439

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return (a*32768 + nextRandom()) % 1000000001
}

func main() {
	arrays := make([][]int64, 10)
	for c := range arrays {
		arrays[c] = make([]int64, 100000)
		for i := range arrays[c] {
			arrays[c][i] = wide()
		}
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for c := range arrays {
			at := (p*7919 + int64(c)*104729) % 100000
			arrays[c][at] = wide()
			check = (check*31 + minimizeArrayValue(arrays[c]) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
