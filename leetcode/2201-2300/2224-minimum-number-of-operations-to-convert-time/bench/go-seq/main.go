// LeetCode #2224: Minimum Number of Operations to Convert Time -- the
// benchmark's Go mirror of convert.kara: each time read from its four
// digits, the gap in minutes cut greedily by 60s, 15s, 5s and 1s.
package main

import "fmt"

func minutesOf(time string) int64 {
	d := []int64{}
	for _, c := range time {
		if c != ':' {
			d = append(d, int64(c-'0'))
		}
	}
	return (d[0]*10+d[1])*60 + d[2]*10 + d[3]
}

func convertTime(current, correct string) int64 {
	gap := minutesOf(correct) - minutesOf(current)
	operations := int64(0)
	for _, step := range []int64{60, 15, 5, 1} {
		operations += gap / step
		gap %= step
	}
	return operations
}

var seed int64 = 2224

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// every time of the day as "HH:MM", built once
	times := make([]string, 1440)
	for m := 0; m < 1440; m++ {
		times[m] = fmt.Sprintf("%02d:%02d", m/60, m%60)
	}
	check := int64(0)
	for i := 0; i < 2000000; i++ {
		a := nextRandom() % 1440
		b := nextRandom() % 1440
		low, high := a, b
		if a > b {
			low, high = b, a
		}
		check = (check*31 + convertTime(times[low], times[high])) % 1000000007
	}
	fmt.Printf("2000000 pairs: checksum %d\n", check)
}
