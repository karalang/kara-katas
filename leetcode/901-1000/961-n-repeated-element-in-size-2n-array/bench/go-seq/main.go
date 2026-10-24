// Benchmark: LeetCode #961 N-Repeated Element in Size 2N Array -- the ★
// arm, near neighbours, on 10000 numbers, LeetCode's largest, with the
// repeated value at every other place. Each call swaps two of the other
// values first. Mirrors ../repeated_n_times.kara, .c, .rs and .py.
package main

import "fmt"

var seed int64 = 961

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func repeatedNTimes(nums []int64) int64 {
	n := len(nums)
	for k := 1; k < 4; k++ {
		for i := 0; i < n-k; i++ {
			if nums[i] == nums[i+k] {
				return nums[i]
			}
		}
	}
	return -1
}

func alternating(n int, first bool) []int64 {
	used := make([]bool, 10001)
	r := nextRandom() % 10001
	used[r] = true
	out := make([]int64, 0, 2*n)
	for len(out) < 2*n {
		v := nextRandom() % 10001
		if !used[v] {
			used[v] = true
			if first {
				out = append(out, r, v)
			} else {
				out = append(out, v, r)
			}
		}
	}
	return out
}

func main() {
	rounds := 1000
	cases := make([][]int64, 50)
	for i := range cases {
		cases[i] = alternating(5000, i%2 == 0)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 50; i++ {
			c := (r + i) % 50
			p := 2*(nextRandom()%4999) + 1 - int64(c%2)
			cases[c][p], cases[c][p+2] = cases[c][p+2], cases[c][p]
			a := repeatedNTimes(cases[c])
			total += a
			check = (check*31 + a + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 50 cases of 10000 numbers: the repeated ones sum to %d, checksum %d\n", rounds, total, check)
}
