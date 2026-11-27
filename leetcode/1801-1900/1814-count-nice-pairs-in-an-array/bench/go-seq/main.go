// LeetCode #1814: Count Nice Pairs in an Array -- the bench in Go: the ★
// arm over 200 calls on runs of 50000 to 99999 numbers cut from one array
// of 10^5, built once, each run's length drawn from the checksum so far.
package main

import "fmt"

const mod = 1000000007

func rev(x int64) int64 {
	var r int64
	for x > 0 {
		r = r*10 + x%10
		x /= 10
	}
	return r
}

func countNicePairs(nums []int64) int64 {
	seen := map[int64]int64{}
	var pairs int64
	for _, x := range nums {
		d := x - rev(x)
		c := seen[d]
		pairs = (pairs + c) % mod
		seen[d] = c + 1
	}
	return pairs
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1814)
	base := make([]int64, 0, 100000)
	for k := 0; k < 100000; k++ {
		if k%2 == 0 {
			base = append(base, nextRandom(&seed)%10000)
		} else {
			hi := nextRandom(&seed)
			base = append(base, (hi*32768+nextRandom(&seed))%1000000001)
		}
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		n := 50000 + (check+call)%50000
		run := make([]int64, n)
		copy(run, base[:n])
		check = (check*31 + countNicePairs(run)) % mod
	}
	fmt.Printf("200 calls: checksum %d\n", check)
}
