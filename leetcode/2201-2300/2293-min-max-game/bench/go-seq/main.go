// LeetCode #2293: Min Max Game -- the bench, the ★ arm in Go. The rounds
// played in place on a copy of the array.
package main

import "fmt"

func minMaxGame(nums []int64) int64 {
	a := append([]int64(nil), nums...)
	n := len(a)
	for n > 1 {
		n /= 2
		for i := 0; i < n; i++ {
			x, y := a[2*i], a[2*i+1]
			if (i%2 == 0) == (x < y) {
				a[i] = x
			} else {
				a[i] = y
			}
		}
	}
	return a[0]
}

var seed int64 = 2293

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 200)
	for k := range arrays {
		nums := make([]int64, 1024)
		for i := range nums {
			hi := nextRandom()
			nums[i] = (hi*32768+nextRandom())%1000000000 + 1
		}
		arrays[k] = nums
	}
	var check int64
	for p := 0; p < 50; p++ {
		var total int64
		for _, nums := range arrays {
			total += minMaxGame(nums)
		}
		check = (check*31 + total) % 1000000007
	}
	fmt.Printf("50 passes over 200 arrays of 1024: checksum %d\n", check)
}
