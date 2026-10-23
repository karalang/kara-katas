// LeetCode #927: Three Equal Parts -- bench: three pointers.
// Mirrors three_equal_parts.kara.
package main

import "fmt"

func threeEqualParts(arr []int64) []int64 {
	n := int64(len(arr))
	var ones int64
	for _, v := range arr {
		ones += v
	}
	if ones == 0 {
		return []int64{0, n - 1}
	}
	if ones%3 != 0 {
		return []int64{-1, -1}
	}
	third := ones / 3
	var starts []int64
	var seen int64
	for k := int64(0); k < n; k++ {
		if arr[k] == 1 {
			if seen%third == 0 {
				starts = append(starts, k)
			}
			seen++
		}
	}
	a, b, c := starts[0], starts[1], starts[2]
	for c < n && arr[a] == arr[b] && arr[b] == arr[c] {
		a++
		b++
		c++
	}
	if c == n {
		return []int64{a - 1, b}
	}
	return []int64{-1, -1}
}

var seed int64 = 927

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count = 30, 100
	// count arrays of 30000 digits, built once: a value of 9000 digits
	// written three times, each copy after up to 1000 leading 0s and the
	// array filled up with 0s in front, and every other array with one
	// digit flipped
	arrays := make([][]int64, count)
	for a := 0; a < count; a++ {
		value := make([]int64, 9000)
		for k := range value {
			value[k] = nextRandom() % 2
		}
		var parts []int64
		for copy := 0; copy < 3; copy++ {
			zeros := nextRandom() % 1001
			for z := int64(0); z < zeros; z++ {
				parts = append(parts, 0)
			}
			parts = append(parts, value...)
		}
		arr := make([]int64, 30000-len(parts), 30000)
		arr = append(arr, parts...)
		if a%2 == 1 {
			at := nextRandom() % 30000
			arr[at] = 1 - arr[at]
		}
		arrays[a] = arr
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every array, starting from a different one
		for i := 0; i < count; i++ {
			got := threeEqualParts(arrays[(r+i)%count])
			if got[0] >= 0 {
				found++
			}
			check = (check*1000003 + got[0] + 1) % 1000000007
			check = (check*1000003 + got[1] + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of 30000: %d split, checksum %d\n", rounds, count, found, check)
}
