// LeetCode #1326 bench, Go mirror of the Kāra bench: the ★ arm (each tap
// turned into how far right it waters from its leftmost point, then the
// garden crossed as a jump game) on 20 gardens of 10^4 built once; then 300
// passes, each setting one tap of every garden from the checksum so far,
// answering it and folding the answer plus the pass into the checksum.
package main

import "fmt"

func minTaps(n32 int32, ranges []int32) int32 {
	n := int64(n32)
	farthest := make([]int64, n+1)
	for i := int64(0); i <= n; i++ {
		r := int64(ranges[i])
		left := i - r
		if left < 0 {
			left = 0
		}
		right := i + r
		if right > n {
			right = n
		}
		if right > farthest[left] {
			farthest[left] = right
		}
	}
	var taps, watered, next int64
	for x := int64(0); x < n; x++ {
		if farthest[x] > next {
			next = farthest[x]
		}
		if x == watered {
			if next <= x {
				return -1
			}
			taps++
			watered = next
		}
	}
	return int32(taps)
}

var seed int64 = 1326

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 10000
	gardens := make([][]int32, 0, 20)
	for t := 0; t < 20; t++ {
		var open int64
		switch t % 4 {
		case 0:
			open = 1
		case 1:
			open = 3
		case 2:
			open = 10
		default:
			open = 30
		}
		ranges := make([]int32, 0, n+1)
		for i := 0; i <= n; i++ {
			var r int64
			if nextRandom()%open == 0 {
				r = 1 + nextRandom()%100
			}
			ranges = append(ranges, int32(r))
		}
		gardens = append(gardens, ranges)
	}
	var check int64
	for pass := int64(0); pass < 300; pass++ {
		for t := 0; t < 20; t++ {
			gardens[t][check%(n+1)] = int32((check / 7) % 101)
			taps := int64(minTaps(n, gardens[t]))
			check = (check*31 + taps + 1 + pass) % 1000000007
		}
	}
	fmt.Printf("300 passes over 20 gardens of 10^4: checksum %d\n", check)
}
