// Benchmark: LeetCode #981 Time Based Key-Value Store -- the ★ arm, a
// list per key and binary search, on LeetCode's largest sessions of
// 200,000 calls. Mirrors ../time_map.kara, .rs, .c and .py.
package main

import "fmt"

type entry struct {
	timestamp int64
	value     string
}

type TimeMap struct {
	store map[string][]entry
}

func NewTimeMap() TimeMap {
	return TimeMap{store: map[string][]entry{}}
}

func (tm *TimeMap) Set(key string, value string, timestamp int64) {
	tm.store[key] = append(tm.store[key], entry{timestamp, value})
}

func (tm *TimeMap) Get(key string, timestamp int64) string {
	list, ok := tm.store[key]
	if !ok {
		return ""
	}
	lo, hi := 0, len(list)
	for lo < hi {
		mid := (lo + hi) / 2
		if list[mid].timestamp <= timestamp {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo == 0 {
		return ""
	}
	return list[lo-1].value
}

var seed int64 = 981

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 20
	calls := 200000
	keys := make([]string, 1000)
	for i := int64(0); i < 1000; i++ {
		keys[i] = fmt.Sprintf("user%d", i*7919%100000)
	}
	values := make([]string, 100)
	for i := int64(0); i < 100; i++ {
		values[i] = fmt.Sprintf("value%d", i*104729%1000000)
	}
	found := 0
	var check int64 = 0
	for r := 0; r < rounds; r++ {
		tm := NewTimeMap()
		var now int64 = 0
		for c := 0; c < calls; c++ {
			k := nextRandom() % 1000
			if nextRandom()%2 == 0 {
				now += 1 + nextRandom()%3
				tm.Set(keys[k], values[nextRandom()%100], now)
			} else {
				t := 1 + nextRandom()%(now+3)
				got := tm.Get(keys[k], t)
				if len(got) > 0 {
					found++
				}
				check = (check*131 + int64(len(got))) % 1000000007
				for i := 0; i < len(got); i++ {
					check = (check*131 + int64(got[i])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds of %d calls on 1000 keys: %d values found, checksum %d\n", rounds, calls, found, check)
}
