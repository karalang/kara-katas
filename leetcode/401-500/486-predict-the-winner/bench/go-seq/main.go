// Benchmark for #486: Go mirror of the ★ arm (one row of leads); see
// ../predict_the_winner.kara.
package main

import "fmt"

func predictTheWinner(nums []int64) bool {
	n := len(nums)
	d := make([]int64, n)
	copy(d, nums)
	for i := n - 2; i >= 0; i-- {
		for j := i + 1; j < n; j++ {
			d[j] = max(nums[i]-d[j], nums[j]-d[j-1])
		}
	}
	return d[n-1] >= 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	arrays := [][]int64{}
	var seed int64 = 486
	for a := 0; a < 200; a++ {
		nums := []int64{}
		for i := 0; i < 1000+a%2; i++ {
			nums = append(nums, nextRandom(&seed)*32768%10000001)
		}
		arrays = append(arrays, nums)
	}
	var wins, checksum int64
	for _, nums := range arrays {
		var win int64
		if predictTheWinner(nums) {
			win = 1
		}
		wins += win
		checksum = (checksum*31 + win*7 + int64(len(nums))) % 1000000007
	}
	fmt.Printf("200 arrays of 1000 or 1001 numbers: player 1 wins %d, checksum %d\n", wins, checksum)
}
