// Benchmark for #852: Peak Index in a Mountain Array -- Go twin of the Kāra
// ★ arm (binary search on the slope).
package main

import "fmt"

func peakIndexInMountainArray(arr []int64) int64 {
	lo, hi := 0, len(arr)-1
	for lo < hi {
		mid := (lo + hi) / 2
		if arr[mid] < arr[mid+1] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return int64(lo)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 64, 30000000
	const n int64 = 100000
	var seed int64 = 852
	arrays := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		step := 1 + g%10
		peak := 1 + (nextRandom(&seed)*32768+nextRandom(&seed))%(n-2)
		arr := make([]int64, 0, n)
		var v, low int64
		for i := int64(0); i < n; i++ {
			if i > 0 {
				if i <= peak {
					v += 1 + nextRandom(&seed)%step
				} else {
					v -= 1 + nextRandom(&seed)%step
				}
			}
			arr = append(arr, v)
			low = min(low, v)
		}
		for i := range arr {
			arr[i] -= low
		}
		arrays = append(arrays, arr)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		p := peakIndexInMountainArray(arrays[round%count])
		total += p
		checksum = (checksum*31 + p) % 1000000007
	}
	fmt.Printf("%d rounds of %d mountains: peaks sum to %d, checksum %d\n", rounds, count, total, checksum)
}
