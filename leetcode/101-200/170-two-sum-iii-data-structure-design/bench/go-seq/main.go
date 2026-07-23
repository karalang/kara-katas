package main

import "fmt"

type TwoSum struct {
	counts map[int64]int64
}

func newTwoSum() *TwoSum {
	return &TwoSum{counts: make(map[int64]int64)}
}

func add(ds *TwoSum, number int64) {
	ds.counts[number]++
}

func find(ds *TwoSum, value int64) bool {
	found := false
	for k := range ds.counts {
		complement := value - k
		if complement == k {
			if ds.counts[k] >= 2 {
				found = true
			}
		} else {
			if _, ok := ds.counts[complement]; ok {
				found = true
			}
		}
	}
	return found
}

func main() {
	var kRange int64 = 6000
	var nAdd int64 = 170
	var mQuery int64 = 1200000

	ds := newTwoSum()
	var state int64 = 12345
	for i := int64(0); i < nAdd; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		add(ds, state%kRange)
	}

	var sink int64 = 0
	for q := int64(0); q < mQuery; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		target := state % (2 * kRange)
		if find(ds, target) {
			sink++
		}
	}
	fmt.Println(sink)
}
