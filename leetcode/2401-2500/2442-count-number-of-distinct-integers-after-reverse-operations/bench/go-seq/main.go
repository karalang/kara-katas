// LeetCode #2442: Count Number of Distinct Integers After Reverse
// Operations -- the bench, the ★ arm: the digits reversed by `% 10` and
// `/ 10`, and a table of flags up to the largest value.
package main

import "fmt"

func reversed(x int64) int64 {
	var r int64
	for y := x; y > 0; y /= 10 {
		r = r*10 + y%10
	}
	return r
}

func countDistinctIntegers(nums []int64) int64 {
	values := append([]int64(nil), nums...)
	for _, x := range nums {
		values = append(values, reversed(x))
	}
	var largest int64
	for _, v := range values {
		if v > largest {
			largest = v
		}
	}
	seen := make([]bool, largest+1)
	var count int64
	for _, v := range values {
		if !seen[v] {
			seen[v] = true
			count++
		}
	}
	return count
}

var seed int64 = 2442

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return 1 + (a*32768+nextRandom())%1000000
}

func main() {
	arrays := make([][]int64, 4)
	for c := range arrays {
		arrays[c] = make([]int64, 100000)
		for i := range arrays[c] {
			arrays[c][i] = wide()
		}
	}
	var check int64
	for p := int64(0); p < 40; p++ {
		for c := range arrays {
			at := (p*7919 + int64(c)*104729) % 100000
			arrays[c][at] = wide()
			check = (check*31 + countDistinctIntegers(arrays[c]) + p) % 1000000007
		}
	}
	fmt.Printf("40 passes over 4 arrays of 10^5 values: checksum %d\n", check)
}
