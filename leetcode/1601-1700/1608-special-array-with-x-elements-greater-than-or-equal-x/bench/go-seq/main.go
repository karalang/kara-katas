// LeetCode #1608: Special Array With X Elements Greater Than or Equal X --
// the bench in Go, mirroring special.kara: the numbers sorted largest
// first, `x` special when the `x`th largest is at least `x` and the next
// is below it.
package main

import (
	"fmt"
	"slices"
)

func specialArray(src []int32) int {
	nums := slices.Clone(src)
	slices.SortFunc(nums, func(a, b int32) int {
		if b < a {
			return -1
		}
		if b > a {
			return 1
		}
		return 0
	})
	n := len(nums)
	for x := 1; x <= n; x++ {
		if int(nums[x-1]) >= x && (x == n || int(nums[x]) < x) {
			return x
		}
	}
	return -1
}

func main() {
	seed := int64(1608)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	problems := make([][]int32, 0, 1000)
	for p := 0; p < 1000; p++ {
		nums := make([]int32, 0, 10000)
		for i := 0; i < 10000; i++ {
			a := nextRandom()
			b := nextRandom()
			nums = append(nums, int32((a*32768+b)%10001))
		}
		problems = append(problems, nums)
	}
	check, special := int64(0), 0
	for _, nums := range problems {
		x := specialArray(nums)
		if x >= 0 {
			special++
		}
		check = (check*31 + int64(x) + 1) % 1000000007
	}
	fmt.Printf("1000 problems of 10000 numbers from 0 to 10000: %d special, checksum %d\n", special, check)
}
