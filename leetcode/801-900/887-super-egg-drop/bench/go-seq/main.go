// LeetCode #887 bench: Go mirror of super_egg_drop.kara (the ★ arm, the
// floors a number of moves can cover) on the same 30000 cases.
package main

import "fmt"

func superEggDrop(k int64, n int64) int64 {
	floors := make([]int64, k+1)
	var moves int64
	for floors[k] < n {
		moves++
		for eggs := k; eggs >= 1; eggs-- {
			floors[eggs] = floors[eggs-1] + floors[eggs] + 1
		}
	}
	return moves
}

var seed int64 = 887

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for c := 0; c < 30000; c++ {
		k := 2 + nextRandom()%8
		hi := nextRandom()
		n := 1 + (hi*32768+nextRandom())%1000000000
		moves := superEggDrop(k, n)
		total += moves
		check = (check*131 + moves) % 1000000007
	}
	fmt.Printf("30000 cases of 2 to 9 eggs and up to 10^9 floors: %d moves, checksum %d\n", total, check)
}
