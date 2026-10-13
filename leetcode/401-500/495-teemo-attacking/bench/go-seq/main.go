// Benchmark for #495: Go mirror of the ★ arm (each gap, capped); see
// ../teemo_attacking.kara.
package main

import "fmt"

func findPoisonedDuration(timeSeries []int64, duration int64) int64 {
	var total int64
	for i := range timeSeries {
		if i+1 < len(timeSeries) {
			total += min(timeSeries[i+1]-timeSeries[i], duration)
		} else {
			total += duration
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 200 series of 10,000 attacks (the problem's most) with gaps of 0
	// to 99, built once, then each solved for every duration from 0 to
	// 49.
	var all [][]int64
	var seed int64 = 495
	for k := 0; k < 200; k++ {
		series := make([]int64, 0, 10000)
		var t int64
		for i := 0; i < 10000; i++ {
			series = append(series, t)
			t += nextRandom(&seed) % 100
		}
		all = append(all, series)
	}
	var total, checksum int64
	for _, series := range all {
		for duration := int64(0); duration < 50; duration++ {
			poisoned := findPoisonedDuration(series, duration)
			total += poisoned
			checksum = (checksum*31 + poisoned) % 1000000007
		}
	}
	fmt.Printf("200 series of 10000, 50 durations each: %d poisoned in all, checksum %d\n", total, checksum)
}
