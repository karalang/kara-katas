// LeetCode #2080: Range Frequency Queries -- Go mirror of the ★ arm's
// benchmark (frequency.kara): 10 arrays of 10^5 values, each built into a
// `map` of every value's places once and then asked 1000000 queries.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 2080

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type RangeFreqQuery struct {
	places map[int64][]int64
}

func newRangeFreqQuery(arr []int64) *RangeFreqQuery {
	places := make(map[int64][]int64)
	for i, v := range arr {
		places[v] = append(places[v], int64(i))
	}
	return &RangeFreqQuery{places}
}

func (q *RangeFreqQuery) query(left, right, value int64) int64 {
	at, ok := q.places[value]
	if !ok {
		return 0
	}
	hi := sort.Search(len(at), func(k int) bool { return at[k] > right })
	lo := sort.Search(len(at), func(k int) bool { return at[k] >= left })
	return int64(hi - lo)
}

func main() {
	const n = 100000
	var total, check int64
	tops := []int64{100, 1000, 10000}
	for t := 0; t < 10; t++ {
		top := tops[t%3]
		arr := make([]int64, n)
		for i := range arr {
			arr[i] = nextRandom()%top + 1
		}
		index := newRangeFreqQuery(arr)
		for k := 0; k < 1000000; k++ {
			a := (nextRandom()*32768 + nextRandom()) % n
			b := (nextRandom()*32768 + nextRandom()) % n
			var value int64
			if nextRandom()%2 == 0 {
				value = arr[(nextRandom()*32768+nextRandom())%n]
			} else {
				value = nextRandom()%(top+1) + 1
			}
			c := index.query(min(a, b), max(a, b), value)
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("10000000 queries: sum %d, checksum %d\n", total, check)
}
