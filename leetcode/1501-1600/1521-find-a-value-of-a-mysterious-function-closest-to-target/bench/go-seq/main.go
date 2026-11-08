// LeetCode #1521: Find a Value of a Mysterious Function Closest to Target
// -- bench: the ★ arm over 2000 random arrays of 1 to 4000 numbers, built
// once and answered 3 times.
package main

import "fmt"

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func closestToTarget(arr []int64, target int64) int64 {
	best := abs(arr[0] - target)
	var ends []int64
	for _, x := range arr {
		next := []int64{x}
		for _, v := range ends {
			w := v & x
			if w != next[len(next)-1] {
				next = append(next, w)
			}
		}
		for _, v := range next {
			if d := abs(v - target); d < best {
				best = d
			}
		}
		ends = next
	}
	return best
}

var seed int64 = 1521

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	const count = 2000
	arrays := make([][]int64, 0, count)
	targets := make([]int64, 0, count)
	for c := 0; c < count; c++ {
		n := nextRandom()%4000 + 1
		base := nextRandom()%1000000 + 1
		arr := make([]int64, 0)
		for i := int64(0); i < n; i++ {
			var x int64
			if nextRandom()%2 == 0 {
				hi := nextRandom()
				x = base & (hi*32768 + nextRandom())
			} else {
				x = nextRandom() * 32 % 1000000
			}
			if x < 1 {
				x = 1
			}
			arr = append(arr, x)
		}
		hi := nextRandom()
		targets = append(targets, (hi*32768+nextRandom())%1000001)
		arrays = append(arrays, arr)
	}
	var check, total int64
	for pass := 0; pass < 3; pass++ {
		for c := 0; c < count; c++ {
			answer := closestToTarget(arrays[c], targets[c])
			total += answer
			check = mix(check, answer)
		}
	}
	fmt.Printf("3 passes over 2000 arrays of up to 4000 numbers: distances sum to %d, checksum %d\n", total, check)
}
