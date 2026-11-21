// LeetCode #2518: Number of Great Partitions -- Go mirror of the benchmark
// (great.kara): the same lists, passes, order and checksum.
package main

import "fmt"

const MOD = 1000000007

func countPartitions(nums []int64, k int64) int64 {
	var total int64
	for _, x := range nums {
		total += x
	}
	if total < 2*k {
		return 0
	}
	ways := make([]int64, k)
	ways[0] = 1
	all := int64(1)
	for _, x := range nums {
		all = all * 2 % MOD
		if x < k {
			for s := k - 1; s >= x; s-- {
				ways[s] = (ways[s] + ways[s-x]) % MOD
			}
		}
	}
	var short int64
	for _, w := range ways {
		short = (short + w) % MOD
	}
	return ((all-2*short)%MOD + MOD) % MOD
}

var seed int64 = 2518

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 20)
	for t := range lists {
		lists[t] = make([]int64, 1000)
		for i := range lists[t] {
			lists[t][i] = nextRandom()%1000 + 1
		}
	}
	const passes = 35
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, nums := range lists {
			check = (check*31 + countPartitions(nums, check%1000+1) + p) % MOD
		}
	}
	fmt.Printf("%d passes over 20 lists of 1000 numbers: checksum %d\n", passes, check)
}
