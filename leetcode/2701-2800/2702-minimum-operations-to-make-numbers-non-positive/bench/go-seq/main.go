// LeetCode #2702: Minimum Operations to Make Numbers Non-positive -- the
// bench (nonpositive.kara in Go): a binary search on the count, each
// trial summing the extra shares the numbers still above t * y need.
package main

import "fmt"

func minOperations(nums []int64, x, y int64) int64 {
	top := nums[0]
	for _, v := range nums {
		if v > top {
			top = v
		}
	}
	low, high := int64(0), top/y+1
	for low < high {
		t := (low + high) / 2
		var need int64
		for _, v := range nums {
			if v > t*y {
				need += (v - t*y + x - y - 1) / (x - y)
				if need > t {
					break
				}
			}
		}
		if need <= t {
			high = t
		} else {
			low = t + 1
		}
	}
	return low
}

var seed int64 = 2702

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

type problem struct {
	nums []int64
	x, y int64
}

func main() {
	arrays, n, rounds := 100, 10000, 5
	problems := make([]problem, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = wide()%1000000000 + 1
		}
		y := nextRandom()%1000 + 1
		x := y + wide()%1000000 + 1
		problems = append(problems, problem{nums, x, y})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range problems {
			t := minOperations(p.nums, p.x, p.y)
			sum += t
			check = (check*31 + t + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d numbers up to 1000000000, %d rounds: operations sum to %d, checksum %d\n", arrays, n, rounds, sum, check)
}
