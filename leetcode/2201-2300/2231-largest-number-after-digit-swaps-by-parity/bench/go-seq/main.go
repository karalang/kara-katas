// LeetCode #2231: Largest Number After Digit Swaps by Parity -- the
// benchmark's Go mirror of parity.kara: each parity's digits sorted from
// largest down into that parity's places.
package main

import (
	"fmt"
	"sort"
	"strconv"
)

func largestInteger(num int64) int64 {
	text := strconv.FormatInt(num, 10)
	digits := make([]int64, len(text))
	for i := range text {
		digits[i] = int64(text[i]) - 48
	}
	odd := []int64{}
	even := []int64{}
	for _, d := range digits {
		if d%2 == 1 {
			odd = append(odd, d)
		} else {
			even = append(even, d)
		}
	}
	sort.Slice(odd, func(i, j int) bool { return odd[i] < odd[j] })
	sort.Slice(even, func(i, j int) bool { return even[i] < even[j] })
	var largest int64
	for _, d := range digits {
		var next int64
		if d%2 == 1 {
			next = odd[len(odd)-1]
			odd = odd[:len(odd)-1]
		} else {
			next = even[len(even)-1]
			even = even[:len(even)-1]
		}
		largest = largest*10 + next
	}
	return largest
}

var seed int64 = 2231

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	nums := make([]int64, 100000)
	for i := range nums {
		nums[i] = wideRandom()%1000000000 + 1
	}
	var check int64
	for r := 0; r < 20; r++ {
		// punch: one num drawn again before each pass over all of them
		at := wideRandom() % 100000
		nums[at] = wideRandom()%1000000000 + 1
		for _, num := range nums {
			check = (check*31 + largestInteger(num)) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10^5 nums: checksum %d\n", check)
}
