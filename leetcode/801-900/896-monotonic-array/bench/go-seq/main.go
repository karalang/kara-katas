// LeetCode #896 bench: the ★ arm (one pass, two flags) over 16 arrays of
// 100,000 numbers, LeetCode's largest, built once as random walks, half
// rising and half falling. Each of 2,000 rounds sets one random place of
// one array to the number before it, which keeps the array monotonic, or
// in every other round to a random number, asks whether the array is
// monotonic, and puts the number back. The same algorithm as
// is_monotonic.kara.
package main

import "fmt"

func isMonotonic(nums []int64) bool {
	rising, falling := true, true
	for i := 1; i < len(nums); i++ {
		if nums[i] > nums[i-1] {
			falling = false
		}
		if nums[i] < nums[i-1] {
			rising = false
		}
	}
	return rising || falling
}

var seed int64 = 896

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var arrays [][]int64
	for k := 0; k < 16; k++ {
		nums := make([]int64, 0, 100000)
		x := int64(100000)
		if k%2 == 0 {
			x = -100000
		}
		for i := 0; i < 100000; i++ {
			nums = append(nums, x)
			step := nextRandom() % 2
			if k%2 == 0 {
				x += step
			} else {
				x -= step
			}
		}
		arrays = append(arrays, nums)
	}
	var monotonic, check int64
	for r := 0; r < 2000; r++ {
		a := nextRandom() % 16
		p := nextRandom() * 32768
		p = (p + nextRandom()) % 100000
		random := nextRandom() * 32768
		random = (random+nextRandom())%200001 - 100000
		old := arrays[a][p]
		value := random
		if nextRandom()%2 == 0 && p > 0 {
			value = arrays[a][p-1]
		}
		arrays[a][p] = value
		got := isMonotonic(arrays[a])
		arrays[a][p] = old
		b := int64(0)
		if got {
			monotonic++
			b = 1
		}
		check = (check*131 + p*2 + b) % 1000000007
	}
	fmt.Printf("2000 rounds over 16 arrays of 100000 numbers: %d monotonic, checksum %d\n", monotonic, check)
}
