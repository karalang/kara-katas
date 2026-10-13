// Benchmark for #503 in Go: the ★ arm (a stack of indices, twice
// around); see ../../next_greater_elements.kara. The answer and the
// stack are fresh slices on every call, as the Kāra arm's are fresh Vecs.
package main

import "fmt"

func nextGreaterElements(nums []int64) []int64 {
	n := len(nums)
	answer := make([]int64, n)
	for i := range answer {
		answer[i] = -1
	}
	var waiting []int
	for i := 0; i < 2*n; i++ {
		x := nums[i%n]
		for len(waiting) > 0 {
			top := waiting[len(waiting)-1]
			if nums[top] >= x {
				break
			}
			answer[top] = x
			waiting = waiting[:len(waiting)-1]
		}
		if i < n {
			waiting = append(waiting, i)
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 120 arrays of 10,000 numbers (the problem's most), from 0 to 9,
	// from the whole range -10^9 to 10^9, or falling, in turn; built
	// once. Then each array is solved 100 times, the sum of its answers
	// folded into a checksum.
	arrays := 120
	rounds := 100
	n := int64(10000)
	seed := int64(503)
	var all [][]int64
	for c := 0; c < arrays; c++ {
		var nums []int64
		for i := int64(0); i < n; i++ {
			if c%3 == 0 {
				nums = append(nums, nextRandom(&seed)%10)
			} else if c%3 == 1 {
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				nums = append(nums, (hi*65536+lo)%2000000001-1000000000)
			} else {
				nums = append(nums, 1000000000-i*200000-nextRandom(&seed)%100000)
			}
		}
		all = append(all, nums)
	}
	var found, checksum int64
	for c := 0; c < arrays; c++ {
		for r := 0; r < rounds; r++ {
			answer := nextGreaterElements(all[c])
			var sum int64
			for _, a := range answer {
				sum += a
				if a != -1 {
					found++
				}
			}
			checksum = (checksum*31 + sum%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d numbers, %d times each: %d with a greater one, checksum %d\n", arrays, n, rounds, found, checksum)
}
