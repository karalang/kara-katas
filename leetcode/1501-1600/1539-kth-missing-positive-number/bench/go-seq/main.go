// LeetCode #1539: Kth Missing Positive Number -- bench: the ★ arm (binary
// search on the count of missing numbers) over 1000 arrays of 1 to 1000
// values and 1000 values of k, built once, every pair asked 5 times. Go
// mirror of kth.kara.
package main

import "fmt"

func findKthPositive(arr []int64, k int64) int64 {
	lo, hi := 0, len(arr)
	for lo < hi {
		mid := (lo + hi) / 2
		if arr[mid]-int64(mid)-1 < k {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return int64(lo) + k
}

var seed int64 = 1539

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	arrays := make([][]int64, 0, 1000)
	for a := 0; a < 1000; a++ {
		n := nextRandom()%1000 + 1
		gap := nextRandom()%4 + 1
		arr := make([]int64, 0, n)
		value := int64(0)
		for i := int64(0); i < n; i++ {
			value += nextRandom()%gap + 1
			arr = append(arr, value)
		}
		arrays = append(arrays, arr)
	}
	ks := make([]int64, 1000)
	for i := range ks {
		ks[i] = nextRandom()%2000 + 1
	}
	check := int64(0)
	for p := 0; p < 5; p++ {
		for _, arr := range arrays {
			for _, k := range ks {
				check = mix(check, findKthPositive(arr, k))
			}
		}
	}
	fmt.Printf("5 passes over 1000 arrays of up to 1000 values and 1000 values of k: checksum %d\n", check)
}
