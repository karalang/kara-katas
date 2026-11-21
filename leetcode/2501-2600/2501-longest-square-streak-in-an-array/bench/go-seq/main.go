// LeetCode #2501: Longest Square Streak in an Array -- Go mirror of the
// benchmark (square.kara): the same arrays, passes and checksum; the
// values in a map[int64]struct{} on every ask.
package main

import (
	"fmt"
	"math"
)

var seed int64 = 2501

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(top int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % top
}

func isqrt(v int64) int64 {
	r := int64(math.Sqrt(float64(v)))
	for r*r > v {
		r--
	}
	for (r+1)*(r+1) <= v {
		r++
	}
	return r
}

func longestSquareStreak(nums []int64) int64 {
	present := make(map[int64]struct{}, len(nums))
	for _, v := range nums {
		present[v] = struct{}{}
	}
	var best int64
	for v := range present {
		r := isqrt(v)
		if _, ok := present[r]; ok && r*r == v {
			continue
		}
		var length int64
		for x := v; ; x = x * x {
			if _, ok := present[x]; !ok {
				break
			}
			length++
		}
		if length > best {
			best = length
		}
	}
	if best >= 2 {
		return best
	}
	return -1
}

func chained(n int64) []int64 {
	out := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		if nextRandom()%4 == 0 {
			out = append(out, below(99999)+2)
		} else {
			v := nextRandom()%19 + 2
			times := nextRandom() % 4
			for t := int64(0); t < times; t++ {
				if v*v <= 100000 {
					v = v * v
				}
			}
			out = append(out, v)
		}
	}
	return out
}

func main() {
	const passes = 32
	const n = 100000
	arrays := make([][]int64, 20)
	for q := range arrays {
		arrays[q] = chained(n)
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for q := 0; q < 20; q++ {
			at := check % n
			was := arrays[q][at]
			arrays[q][at] = (check+p)%99999 + 2
			check = (check*31 + longestSquareStreak(arrays[q]) + 1 + p) % 1000000007
			arrays[q][at] = was
		}
	}
	fmt.Printf("%d passes over 20 arrays of 10^5: checksum %d\n", passes, check)
}
