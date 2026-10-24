// Benchmark: LeetCode #978 Longest Turbulent Subarray -- the ★ arm, two
// running lengths, on 20 arrays of 40000 values. Mirrors
// max_turbulence_size.kara, .rs, .c and .py.
package main

import "fmt"

func maxTurbulenceSize(arr []int64) int64 {
	var best, up, down int64 = 1, 1, 1
	for i := 1; i < len(arr); i++ {
		if arr[i-1] < arr[i] {
			up = down + 1
			down = 1
		} else if arr[i-1] > arr[i] {
			down = up + 1
			up = 1
		} else {
			up = 1
			down = 1
		}
		best = max(best, up, down)
	}
	return best
}

var seed int64 = 978

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 150, 20
	arrays := make([][]int64, count)
	for c := range arrays {
		arrays[c] = make([]int64, 40000)
		for i := range arrays[c] {
			arrays[c][i] = nextRandom() % 100
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := maxTurbulenceSize(arrays[(r+i)%count])
			total += k
			check = (check*31 + k) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of 40000 values: lengths total %d, checksum %d\n", rounds, count, total, check)
}
