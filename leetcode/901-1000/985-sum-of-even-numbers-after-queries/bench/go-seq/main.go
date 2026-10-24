// Benchmark: LeetCode #985 Sum of Even Numbers After Queries -- the ★ arm, a
// running sum, on LeetCode's largest: 10000 values and 10000 queries.
// Mirrors ../sum_even_after_queries.kara, .rs, .c and .py.
package main

import "fmt"

func sumEvenAfterQueries(nums []int64, queries [][2]int64) []int64 {
	a := make([]int64, len(nums))
	copy(a, nums)
	var even int64
	for _, x := range a {
		if x%2 == 0 {
			even += x
		}
	}
	var answer []int64
	for _, q := range queries {
		val, index := q[0], q[1]
		if a[index]%2 == 0 {
			even -= a[index]
		}
		a[index] += val
		if a[index]%2 == 0 {
			even += a[index]
		}
		answer = append(answer, even)
	}
	return answer
}

var seed int64 = 985

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 300
	type kase struct {
		nums    []int64
		queries [][2]int64
	}
	var cases []kase
	for c := 0; c < 20; c++ {
		var k kase
		for i := 0; i < 10000; i++ {
			k.nums = append(k.nums, nextRandom()%20001-10000)
		}
		for i := 0; i < 10000; i++ {
			val := nextRandom()%20001 - 10000
			k.queries = append(k.queries, [2]int64{val, nextRandom() % 10000})
		}
		cases = append(cases, k)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := cases[(r+i)%20]
			answer := sumEvenAfterQueries(k.nums, k.queries)
			last := answer[len(answer)-1]
			total += last
			check = (check*31 + (last%1000000007+1000000007)%1000000007) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 cases of 10000 values and 10000 queries: sum %d, checksum %d\n", rounds, total, check)
}
