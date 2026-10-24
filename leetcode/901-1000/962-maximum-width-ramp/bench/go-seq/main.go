// Benchmark: LeetCode #962 Maximum Width Ramp -- the ★ arm, decreasing
// stack, on 50000 numbers, LeetCode's largest, falling overall with
// noise. Each call first sets one number to a new random value. Mirrors
// ../max_width_ramp.kara, .c, .rs and .py.
package main

import "fmt"

var seed int64 = 962

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxWidthRamp(nums []int64) int64 {
	n := len(nums)
	var stack []int
	for i := 0; i < n; i++ {
		if len(stack) == 0 || nums[i] < nums[stack[len(stack)-1]] {
			stack = append(stack, i)
		}
	}
	var best int64
	for j := n - 1; j >= 0 && len(stack) > 0; j-- {
		for len(stack) > 0 && nums[stack[len(stack)-1]] <= nums[j] {
			if w := int64(j - stack[len(stack)-1]); w > best {
				best = w
			}
			stack = stack[:len(stack)-1]
		}
	}
	return best
}

func falling(n, step, noise int64) []int64 {
	out := make([]int64, n)
	for p := int64(0); p < n; p++ {
		out[p] = 50000 - noise - p/step + nextRandom()%(noise+1)
	}
	return out
}

func main() {
	rounds := 40
	cases := make([][]int64, 50)
	for i := range cases {
		cases[i] = falling(50000, int64(1+i%5), int64(10*(i/5)))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 50; i++ {
			c := (r + i) % 50
			p := nextRandom() % 50000
			cases[c][p] = nextRandom() % 50001
			w := maxWidthRamp(cases[c])
			total += w
			check = (check*31 + w + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 50 cases of 50000 numbers: the ramps sum to %d, checksum %d\n", rounds, total, check)
}
