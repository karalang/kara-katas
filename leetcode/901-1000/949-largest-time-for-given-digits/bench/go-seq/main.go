// Benchmark: LeetCode #949 Largest Time for Given Digits -- the ★ arm,
// every arrangement, on all 10000 arrays of four digits. Mirrors
// largest_time_from_digits.kara, .c, .rs and .py.
package main

import "fmt"

func largestTimeFromDigits(arr []int64) string {
	best := int64(-1)
	for i := 0; i < 4; i++ {
		for j := 0; j < 4; j++ {
			if j == i {
				continue
			}
			for k := 0; k < 4; k++ {
				if k == i || k == j {
					continue
				}
				l := 6 - i - j - k
				hours := arr[i]*10 + arr[j]
				minutes := arr[k]*10 + arr[l]
				if hours < 24 && minutes < 60 {
					best = max(best, hours*60+minutes)
				}
			}
		}
	}
	if best < 0 {
		return ""
	}
	return fmt.Sprintf("%d%d:%d%d", best/600, best/60%10, best%60/10, best%10)
}

func main() {
	rounds, count := 500, 10000
	arrays := make([][]int64, 0, count)
	for a := int64(0); a < int64(count); a++ {
		arrays = append(arrays, []int64{a / 1000, a / 100 % 10, a / 10 % 10, a % 10})
	}
	var times, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			s := largestTimeFromDigits(arrays[(r*37+i)%count])
			var v int64
			for c := 0; c < len(s); c++ {
				v = v*131 + int64(s[c])
			}
			if len(s) > 0 {
				times++
			}
			check = (check*1000003 + v) % 1000000007
		}
	}
	fmt.Printf("%d rounds over all %d arrays of four digits: %d times, checksum %d\n", rounds, count, times, check)
}
