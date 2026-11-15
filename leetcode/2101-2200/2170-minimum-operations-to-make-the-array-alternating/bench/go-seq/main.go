// LeetCode #2170: Minimum Operations to Make the Array Alternating -- the
// benchmark's Go mirror of alternating.kara.
package main

import "fmt"

type pair struct{ value, count int64 }

func topTwo(nums []int64, start int) (pair, pair) {
	counts := map[int64]int64{}
	for i := start; i < len(nums); i += 2 {
		counts[nums[i]]++
	}
	var first, second pair
	for value, count := range counts {
		if count > first.count {
			second = first
			first = pair{value, count}
		} else if count > second.count {
			second = pair{value, count}
		}
	}
	return first, second
}

func minimumOperations(nums []int64) int64 {
	n := int64(len(nums))
	ef, es := topTwo(nums, 0)
	of, os := topTwo(nums, 1)
	if ef.value != of.value {
		return n - ef.count - of.count
	}
	a, b := ef.count+os.count, es.count+of.count
	if a > b {
		return n - a
	}
	return n - b
}

var seed int64 = 2170

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]int64, 0, 400000)
	for i := 0; i < 400000; i++ {
		a := nextRandom()
		b := nextRandom()
		row = append(row, (a*32768+b)%1000+1)
	}
	var check int64
	for r := 0; r < 100; r++ {
		a := nextRandom()
		b := nextRandom()
		start := (a*32768 + b) % 300001
		ops := minimumOperations(row[start : start+100000])
		check = (check*31 + ops) % 1000000007
	}
	fmt.Printf("100 solves: checksum %d\n", check)
}
