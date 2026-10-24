// Benchmark: LeetCode #982 Triples with Bitwise AND Equal To Zero -- the
// ★ arm, pair counts and the free bits' submasks, on lists of LeetCode's
// largest size. Mirrors ../count_triplets.kara, .rs, .c and .py.
package main

import "fmt"

func countTriplets(nums []int64) int64 {
	var all int64
	for _, x := range nums {
		all |= x
	}
	var size int64 = 1
	for size <= all {
		size *= 2
	}
	full := size - 1
	pairs := make([]int64, size)
	for _, a := range nums {
		for _, b := range nums {
			pairs[a&b]++
		}
	}
	var triples int64
	for _, x := range nums {
		free := full ^ x
		s := free
		for {
			triples += pairs[s]
			if s == 0 {
				break
			}
			s = (s - 1) & free
		}
	}
	return triples
}

var seed int64 = 982

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 15
	lists := make([][]int64, 20)
	for l := range lists {
		lists[l] = make([]int64, 1000)
		for i := range lists[l] {
			lists[l][i] = nextRandom() % 65536
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			t := countTriplets(lists[(r+i)%20])
			total += t
			check = (check*31 + t) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 lists of 1000 values: triples %d, checksum %d\n", rounds, total, check)
}
