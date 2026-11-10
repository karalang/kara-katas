// Benchmark: LeetCode #1095 Find in Mountain Array -- Go mirror of
// find_in_mountain_array.kara: the ★ arm's three binary searches through a
// counted `get` (an atomic counter, as Kāra's `Atomic[i64]`), over 64
// mountains of 10^4 values built once, 100 rounds of 64 targets each.
package main

import (
	"fmt"
	"sync/atomic"
)

type MountainArray struct {
	values []int32
	calls  atomic.Int64
}

func (m *MountainArray) get(index int32) int32 {
	m.calls.Add(1)
	return m.values[index]
}

func (m *MountainArray) length() int32 {
	return int32(len(m.values))
}

func findInMountainArray(target int32, mountain *MountainArray) int32 {
	n := mountain.length()
	lo, hi := int32(0), n-1
	for lo < hi {
		mid := (lo + hi) / 2
		if mountain.get(mid) < mountain.get(mid+1) {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	peak := lo
	lo, hi = 0, peak
	for lo <= hi {
		mid := (lo + hi) / 2
		v := mountain.get(mid)
		if v == target {
			return mid
		}
		if v < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	lo, hi = peak+1, n-1
	for lo <= hi {
		mid := (lo + hi) / 2
		v := mountain.get(mid)
		if v == target {
			return mid
		}
		if v > target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

var seed int64 = 1095

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	mountains := make([]*MountainArray, 0, 64)
	for j := int64(0); j < 64; j++ {
		up := 1 + j*9997/63
		down := 9999 - up
		v := []int32{int32(down*50000 + nextRandom()%20)}
		for i := int64(0); i < up; i++ {
			v = append(v, v[len(v)-1]+1+int32(nextRandom()%50000))
		}
		for i := int64(0); i < down; i++ {
			v = append(v, v[len(v)-1]-1-int32(nextRandom()%50000))
		}
		mountains = append(mountains, &MountainArray{values: v})
	}
	var found, check int64
	for round := int64(0); round < 100; round++ {
		for _, m := range mountains {
			for q := int64(0); q < 64; q++ {
				k := (round*7919 + q*104729) % 10000
				target := m.values[k] + int32((round+q)%3) - 1
				at := findInMountainArray(target, m)
				if at >= 0 {
					found++
				}
				check = (check*31 + int64(at) + 1) % 1000000007
			}
		}
	}
	var calls int64
	for _, m := range mountains {
		calls += m.calls.Load()
	}
	fmt.Printf("100 rounds over 64 mountains of 10^4 values: %d of 409600 found, %d calls of get, checksum %d\n", found, calls, check)
}
