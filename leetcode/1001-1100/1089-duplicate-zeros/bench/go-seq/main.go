// Benchmark: LeetCode #1089 Duplicate Zeros -- mirrors duplicate_zeros.kara:
// count the zeros, then walk back from the end writing each digit at its
// place shifted by the zeros up to it, over 200 random arrays of 10^4
// digits built once, each copied and duplicated in each of 100 rounds.
package main

import "fmt"

func duplicateZeros(arr []int64) {
	n := int64(len(arr))
	var zeros int64
	for _, x := range arr {
		if x == 0 {
			zeros++
		}
	}
	for i := n - 1; i >= 0; i-- {
		if i+zeros < n {
			arr[i+zeros] = arr[i]
		}
		if arr[i] == 0 {
			zeros--
			if i+zeros < n {
				arr[i+zeros] = 0
			}
		}
	}
}

var seed int64 = 1089

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 200)
	for k := 0; k < 200; k++ {
		arr := make([]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			r := nextRandom() % 15
			if r < 5 {
				arr = append(arr, 0)
			} else {
				arr = append(arr, r-5)
			}
		}
		arrays = append(arrays, arr)
	}
	var zeros, check int64
	for round := int64(0); round < 100; round++ {
		for k, a := range arrays {
			work := append([]int64(nil), a...)
			duplicateZeros(work)
			at := (round*7919 + int64(k)*31) % 10000
			if work[at] == 0 {
				zeros++
			}
			check = (check*31 + work[at]*10 + work[9999]) % 1000000007
		}
	}
	fmt.Printf("100 rounds over 200 arrays of 10^4 digits: %d zeros sampled, checksum %d\n", zeros, check)
}
