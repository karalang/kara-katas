// LeetCode #2528: Maximize the Minimum Powered City -- Go mirror of the
// benchmark (power.kara): the same cities, passes, order and checksum.
package main

import "fmt"

func reachable(power []int64, r, k, target int64) bool {
	n := int64(len(power))
	ends := make([]int64, n+1)
	var running, used int64
	for i := int64(0); i < n; i++ {
		running += ends[i]
		have := power[i] + running
		if have < target {
			need := target - have
			used += need
			if used > k {
				return false
			}
			running += need
			ends[min(i+2*r+1, n)] -= need
		}
	}
	return true
}

func maxPower(stations []int64, r, k int64) int64 {
	n := int64(len(stations))
	prefix := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		prefix[i+1] = prefix[i] + stations[i]
	}
	power := make([]int64, n)
	lo := int64(-1)
	for i := int64(0); i < n; i++ {
		power[i] = prefix[min(i+r+1, n)] - prefix[max(i-r, 0)]
		if lo == -1 || power[i] < lo {
			lo = power[i]
		}
	}
	hi := lo + k
	for lo < hi {
		mid := lo + (hi-lo+1)/2
		if reachable(power, r, k, mid) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

var seed int64 = 2528

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	stations := make([]int64, 100000)
	for i := range stations {
		stations[i] = nextRandom() % 100001
	}
	const passes = 20
	var check int64
	for p := int64(0); p < passes; p++ {
		r := check % 100
		k := 1000000000 - check%1000
		check = (check*31 + maxPower(stations, r, k) + p) % 1000000007
	}
	fmt.Printf("%d passes over 100000 cities: checksum %d\n", passes, check)
}
