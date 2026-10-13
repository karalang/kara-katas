// Benchmark for #539: Go mirror of the ★ arm (minutes, sorted); see
// ../find_min_difference.kara.
package main

import (
	"fmt"
	"slices"
	"strconv"
)

func minutes(t string) int64 {
	h, _ := strconv.ParseInt(t[0:2], 10, 64)
	m, _ := strconv.ParseInt(t[3:5], 10, 64)
	return h*60 + m
}

func findMinDifference(timePoints []string) int64 {
	mins := make([]int64, len(timePoints))
	for i, t := range timePoints {
		mins[i] = minutes(t)
	}
	slices.Sort(mins)
	best := mins[0] + 1440 - mins[len(mins)-1]
	for i := 1; i < len(mins); i++ {
		best = min(best, mins[i]-mins[i-1])
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func clock(minute int64) string {
	return fmt.Sprintf("%02d:%02d", minute/60, minute%60)
}

func main() {
	// 300 lists of 20 to 1,440 distinct times, the first places of a
	// shuffle of the whole day, built once. Then the answer for each
	// list is found 100 times.
	lists := 300
	seed := int64(539)
	day := make([]int64, 1440)
	for m := range day {
		day[m] = int64(m)
	}
	all := make([][]string, lists)
	var totalTimes int64
	for l := 0; l < lists; l++ {
		size := 20 + nextRandom(&seed)%1421
		times := make([]string, size)
		for i := int64(0); i < size; i++ {
			j := i + nextRandom(&seed)%(1440-i)
			day[i], day[j] = day[j], day[i]
			times[i] = clock(day[i])
		}
		totalTimes += size
		all[l] = times
	}
	var total, checksum int64
	for r := 0; r < 100; r++ {
		for _, times := range all {
			answer := findMinDifference(times)
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d lists, %d times, 100 times each: total %d, checksum %d\n", lists, totalTimes, total, checksum)
}
