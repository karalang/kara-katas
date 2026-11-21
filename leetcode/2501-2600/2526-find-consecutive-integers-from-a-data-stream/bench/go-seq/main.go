// LeetCode #2526: Find Consecutive Integers from a Data Stream -- Go mirror
// of the benchmark (stream.kara): the same numbers and passes, each a fresh
// stream fed every number.
package main

import "fmt"

type DataStream struct {
	value, k, run int64
}

func newDataStream(value, k int64) *DataStream {
	return &DataStream{value: value, k: k}
}

func (s *DataStream) consec(num int64) bool {
	if num == s.value {
		s.run++
	} else {
		s.run = 0
	}
	return s.run >= s.k
}

var seed int64 = 2526

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	nums := make([]int64, 100000)
	for i := range nums {
		nums[i] = nextRandom()%3 + 1
	}
	const passes = 1250
	var check int64
	for p := int64(0); p < passes; p++ {
		s := newDataStream(check%3+1, check%8+1)
		var trues int64
		for _, num := range nums {
			if s.consec(num) {
				trues++
			}
		}
		check = (check*31 + trues + p) % 1000000007
	}
	fmt.Printf("%d passes over 10^5 numbers: checksum %d\n", passes, check)
}
