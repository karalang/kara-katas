// LeetCode #681: Next Closest Time -- step a minute at a time. Bench.
package main

import "fmt"

func digitsOf(minutes int64) [4]int64 {
	h, m := minutes/60, minutes%60
	return [4]int64{h / 10, h % 10, m / 10, m % 10}
}

func nextClosestTime(time string) string {
	h := int64(time[0]-'0')*10 + int64(time[1]-'0')
	m := int64(time[3]-'0')*10 + int64(time[4]-'0')
	var allowed [10]bool
	for _, d := range digitsOf(h*60 + m) {
		allowed[d] = true
	}
	now := h*60 + m
	for {
		now = (now + 1) % 1440
		ok := true
		for _, d := range digitsOf(now) {
			if !allowed[d] {
				ok = false
			}
		}
		if ok {
			return fmt.Sprintf("%d%d:%d%d", now/600, now/60%10, now%60/10, now%10)
		}
	}
}

func main() {
	const rounds = 300
	times := make([]string, 1440)
	for t := 0; t < 1440; t++ {
		times[t] = fmt.Sprintf("%02d:%02d", t/60, t%60)
	}
	var sum, wrapped int64
	for r := int64(0); r < rounds; r++ {
		for k := int64(0); k < 1440; k++ {
			at := (k*7 + r) % 1440
			answer := nextClosestTime(times[at])
			hour := int64(answer[0]-'0')*10 + int64(answer[1]-'0')
			then := hour*60 + int64(answer[3]-'0')*10 + int64(answer[4]-'0')
			if then <= at {
				wrapped++
			}
			sum = (sum*1441 + then + 1) % 1000000007
		}
	}
	fmt.Printf("%d times: %d answers on the next day, checksum %d\n", 1440*rounds, wrapped, sum)
}
