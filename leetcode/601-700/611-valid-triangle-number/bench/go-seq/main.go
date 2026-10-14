// Benchmark mirror for #611: the same workload and algorithm as
// triangle_number.kara (sort, then two pointers).
package main

import (
	"fmt"
	"slices"
)

func triangleNumber(nums []int64) int64 {
	a := slices.Clone(nums)
	slices.Sort(a)
	var count int64
	for k := 2; k < len(a); k++ {
		i, j := 0, k-1
		for i < j {
			if a[i]+a[j] > a[k] {
				count += int64(j - i)
				j--
			} else {
				i++
			}
		}
	}
	return count
}

var seed int64 = 611

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays, rounds := int64(20), int64(600)
	all := make([][]int64, 0, arrays)
	for c := int64(0); c < arrays; c++ {
		bound := 100 + step()%901
		nums := make([]int64, 1000)
		for k := range nums {
			nums[k] = step() % (bound + 1)
		}
		all = append(all, nums)
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		got := triangleNumber(all[(r*7)%arrays])
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d arrays, %d rounds: %d triangles, checksum %d\n", arrays, rounds, total, checksum)
}
