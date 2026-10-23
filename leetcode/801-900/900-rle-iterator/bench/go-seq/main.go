// LeetCode #900: RLE Iterator -- bench program, Go.
//
// The offset arm (the encoding left as it is) over one encoding of
// 200,000 runs of 1 to 1,000 terms with values up to 10^9, built once. Each
// round hands the encoding to a fresh iterator, asks for 1 to 1,000 terms
// at a time until the iterator answers -1, folds the answers into a
// checksum, takes the encoding back and changes one run's count.
package main

import "fmt"

type RLEIterator struct {
	encoding []int64
	i        int
	used     int64
}

func newRLEIterator(encoding []int64) *RLEIterator {
	return &RLEIterator{encoding: encoding}
}

func (it *RLEIterator) Next(n int64) int64 {
	need := n
	for it.i < len(it.encoding) {
		left := it.encoding[it.i] - it.used
		if left >= need {
			it.used += need
			return it.encoding[it.i+1]
		}
		need -= left
		it.i += 2
		it.used = 0
	}
	return -1
}

var seed int64 = 900

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var runs int64 = 200000
	var rounds int64 = 140
	encoding := make([]int64, 0, 2*runs)
	for j := int64(0); j < runs; j++ {
		encoding = append(encoding, 1+nextRandom()%1000)
		hi := nextRandom()
		lo := nextRandom()
		encoding = append(encoding, (hi*32768+lo)%1000000001)
	}
	var check, calls int64
	for round := int64(0); round < rounds; round++ {
		it := newRLEIterator(encoding)
		for {
			got := it.Next(1 + nextRandom()%1000)
			calls++
			if got == -1 {
				break
			}
			check = (check*31 + got) % 1000000007
		}
		encoding = it.encoding
		encoding[2*(round*7919%runs)] = 1 + nextRandom()%1000
	}
	fmt.Printf("%d rounds over %d runs: %d calls, checksum %d\n", rounds, runs, calls, check)
}
