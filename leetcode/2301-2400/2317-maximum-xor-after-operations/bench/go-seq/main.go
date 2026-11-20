// LeetCode #2317: Maximum XOR After Operations -- the bench, the ★ arm in
// Go. The operation can clear any of a number's bits and set none, so the
// most is the OR of all the numbers.
package main

import "fmt"

func maximumXor(nums []int64) int64 {
	var all int64
	for _, x := range nums {
		all |= x
	}
	return all
}

var seed int64 = 2317

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 20)
	for a := 0; a < 20; a++ {
		var mask int64
		for k := 0; k < a+4; k++ {
			mask |= 1 << (nextRandom() % 27)
		}
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			hi := nextRandom()
			nums = append(nums, ((hi*32768+nextRandom())%100000001)&mask)
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for p := 0; p < 100; p++ {
		for a := 0; a < 20; a++ {
			check = (check*31 + maximumXor(arrays[(a+p)%20])) % 1000000007
		}
	}
	fmt.Printf("100 passes over 20 arrays of 10^5 numbers: checksum %d\n", check)
}
