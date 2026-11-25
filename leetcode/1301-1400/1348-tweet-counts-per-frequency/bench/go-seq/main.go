// LeetCode #1348 bench -- Go: each name's times in the order recorded; a
// query walks every time of its name into per-chunk counts.
package main

import "fmt"

type TweetCounts struct {
	times map[string][]int32
}

func NewTweetCounts() *TweetCounts {
	return &TweetCounts{times: map[string][]int32{}}
}

func (tc *TweetCounts) RecordTweet(name string, time int32) {
	tc.times[name] = append(tc.times[name], time)
}

func (tc *TweetCounts) GetTweetCountsPerFrequency(freq, name string, start, end int32) []int32 {
	var size int32
	switch freq {
	case "minute":
		size = 60
	case "hour":
		size = 3600
	default:
		size = 86400
	}
	counts := make([]int32, (end-start)/size+1)
	for _, t := range tc.times[name] {
		if t >= start && t <= end {
			counts[(t-start)/size]++
		}
	}
	return counts
}

func main() {
	names := []string{"n0", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9"}
	freqs := []string{"minute", "hour", "day"}
	var seed int64 = 1348
	next := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	tc := NewTweetCounts()
	for i := 0; i < 100000; i++ {
		name := names[next()%10]
		tc.RecordTweet(name, int32(next()%1000001))
	}
	var check int64
	for r := int64(0); r < 10000; r++ {
		tc.RecordTweet(names[check%10], int32(check%1000001))
		start := (check / 11) % 990001
		counts := tc.GetTweetCountsPerFrequency(freqs[(check/13)%3], names[(check/17)%10], int32(start), int32(start+10000))
		for _, n := range counts {
			check = (check*31 + int64(n)) % 1000000007
		}
		check = (check*31 + r) % 1000000007
	}
	fmt.Printf("10000 rounds over 100000 tweets: checksum %d\n", check)
}
