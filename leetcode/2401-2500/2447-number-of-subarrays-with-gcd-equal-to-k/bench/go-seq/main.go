// LeetCode #2447: Number of Subarrays With GCD Equal to K -- the bench,
// the ★ arm: from each start the running GCD, the walk stopped once it
// is no multiple of `k`.
package main

import "fmt"

func gcd(a, b int64) int64 {
	x, y := a, b
	for y != 0 {
		x, y = y, x%y
	}
	return x
}

func subarrayGcd(nums []int64, k int64) int64 {
	var count int64
	for i := range nums {
		var g int64
		for j := i; j < len(nums); j++ {
			g = gcd(g, nums[j])
			if g%k != 0 {
				break
			}
			if g == k {
				count++
			}
		}
	}
	return count
}

var seed int64 = 2447

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw() int64 {
	v := 6 * (1 + nextRandom()%1000)
	if nextRandom()%40 == 0 {
		return v + 1
	}
	return v
}

func main() {
	var arrays [][]int64
	for c := 0; c < 20; c++ {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = draw()
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for p := int64(0); p < 90; p++ {
		for c := range arrays {
			arrays[c][(37*p+int64(c))%1000] = draw()
			check = (check*31 + subarrayGcd(arrays[c], 6) + p) % 1000000007
		}
	}
	fmt.Printf("90 passes over 20 arrays of 1000 values: checksum %d\n", check)
}
