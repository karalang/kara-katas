// LeetCode #2090: K Radius Subarray Averages -- Go mirror of the ★ arm's
// benchmark (averages.kara): the same 30 arrays, each asked for the same 10
// radii, one slide of the window into a fresh slice each.
package main

import "fmt"

var seed int64 = 2090

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func getAverages(nums []int64, k int) []int64 {
	n := len(nums)
	width := 2*k + 1
	avgs := make([]int64, n)
	for i := range avgs {
		avgs[i] = -1
	}
	var sum int64
	for i := 0; i < n; i++ {
		sum += nums[i]
		if i >= width {
			sum -= nums[i-width]
		}
		if i+1 >= width {
			avgs[i-k] = sum / int64(width)
		}
	}
	return avgs
}

func main() {
	arrays := make([][]int64, 30)
	for t := range arrays {
		arrays[t] = make([]int64, 100000)
		for i := range arrays[t] {
			arrays[t][i] = nextRandom() % 100001
		}
	}
	radii := []int{0, 1, 3, 10, 30, 100, 300, 1000, 3000, 20000}
	var total, check int64
	for _, nums := range arrays {
		for _, k := range radii {
			var s int64
			for _, a := range getAverages(nums, k) {
				s += a
			}
			total += s
			check = (check*31 + s) % 1000000007
		}
	}
	fmt.Printf("300 answers: sum %d, checksum %d\n", total, check)
}
