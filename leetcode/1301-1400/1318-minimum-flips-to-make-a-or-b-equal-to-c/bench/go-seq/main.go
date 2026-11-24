// LeetCode #1318 bench, Go mirror of the Kāra bench: the ★ arm (each of the
// 30 bits looked at alone and costed) on 1000 triples of numbers from 1 to
// 10^9 built once; then 3000 passes, each setting one number of every
// triple from the checksum so far, and folding every answer plus the pass
// into the checksum.
package main

import "fmt"

func minFlips(a, b, c int64) int64 {
	var flips int64
	for i := 0; i < 30; i++ {
		x := (a >> i) & 1
		y := (b >> i) & 1
		z := (c >> i) & 1
		if z == 1 {
			flips += 1 - (x | y)
		} else {
			flips += x + y
		}
	}
	return flips
}

var seed int64 = 1318

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const big = 1000000000
	nums := make([]int64, 3000)
	for i := range nums {
		hi := nextRandom()
		nums[i] = 1 + (hi*32768+nextRandom())%big
	}
	var check int64
	for pass := int64(0); pass < 3000; pass++ {
		for t := int64(0); t < 1000; t++ {
			nums[3*t+check%3] = 1 + (check*7919)%big
			got := minFlips(nums[3*t], nums[3*t+1], nums[3*t+2])
			check = (check*31 + got + pass) % 1000000007
		}
	}
	fmt.Printf("3000 passes over 1000 triples: checksum %d\n", check)
}
