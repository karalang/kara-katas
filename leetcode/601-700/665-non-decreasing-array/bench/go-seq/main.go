// Benchmark for #665: fix each drop as it comes, as the Kara ★ arm.
package main

import "fmt"

func checkPossibility(nums []int64) bool {
	a := make([]int64, len(nums))
	copy(a, nums)
	fixes := 0
	for i := 1; i < len(a); i++ {
		if a[i] < a[i-1] {
			fixes++
			if fixes > 1 {
				return false
			}
			if i < 2 || a[i-2] <= a[i] {
				a[i-1] = a[i]
			} else {
				a[i] = a[i-1]
			}
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(665)
	arrays := make([][]int64, 0, 16)
	for t := 0; t < 16; t++ {
		v := make([]int64, 0, 10000)
		x := int64(-100000)
		for i := 0; i < 10000; i++ {
			v = append(v, x)
			x += nextRandom(&seed) % 21
		}
		for k := 0; k < t%3; k++ {
			at := nextRandom(&seed) % 10000
			v[at] = nextRandom(&seed)%200001 - 100000
		}
		arrays = append(arrays, v)
	}
	rounds := int64(40000)
	var yes, sum int64
	for r := int64(0); r < rounds; r++ {
		ok := checkPossibility(arrays[r%16])
		b := int64(0)
		if ok {
			yes++
			b = 1
		}
		sum = (sum*31 + r*2 + b) % 1000000007
	}
	fmt.Printf("16 arrays of 10000, %d rounds: %d can be sorted, checksum %d\n", rounds, yes, sum)
}
