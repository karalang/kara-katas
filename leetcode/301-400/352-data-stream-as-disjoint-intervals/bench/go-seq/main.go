// Bench mirror of summary_ranges.kara (the sorted-vector arm), same algorithm.
package main

import "fmt"

type SummaryRanges struct {
	starts, ends []int64
}

func (sr *SummaryRanges) firstAfter(value int64) int {
	lo, hi := 0, len(sr.starts)
	for lo < hi {
		mid := (lo + hi) / 2
		if sr.starts[mid] <= value {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func (sr *SummaryRanges) addNum(value int64) {
	i := sr.firstAfter(value)
	joinsLeft := i > 0 && sr.ends[i-1] >= value-1
	if i > 0 && sr.ends[i-1] >= value {
		return
	}
	joinsRight := i < len(sr.starts) && sr.starts[i] == value+1
	if joinsLeft && joinsRight {
		sr.ends[i-1] = sr.ends[i]
		sr.starts = append(sr.starts[:i], sr.starts[i+1:]...)
		sr.ends = append(sr.ends[:i], sr.ends[i+1:]...)
	} else if joinsLeft {
		sr.ends[i-1] = value
	} else if joinsRight {
		sr.starts[i] = value
	} else {
		sr.starts = append(sr.starts, 0)
		copy(sr.starts[i+1:], sr.starts[i:])
		sr.starts[i] = value
		sr.ends = append(sr.ends, 0)
		copy(sr.ends[i+1:], sr.ends[i:])
		sr.ends[i] = value
	}
}

func (sr *SummaryRanges) getIntervals() [][2]int64 {
	out := make([][2]int64, 0)
	for i := range sr.starts {
		out = append(out, [2]int64{sr.starts[i], sr.ends[i]})
	}
	return out
}

func nextValue(state *int64, limit int64) int64 {
	*state = (*state*1103515245 + 12345) % 2147483648
	return (*state >> 8) % (limit + 1)
}

func main() {
	var rounds int64 = 150
	var sink int64
	for r := int64(0); r < rounds; r++ {
		stream := &SummaryRanges{}
		state := 352 + r
		for i := 1; i < 30001; i++ {
			stream.addNum(nextValue(&state, 10000))
			if i%3000 == 0 {
				for _, iv := range stream.getIntervals() {
					sink = (sink*31 + iv[0]*7 + iv[1] + r) % 1000000007
				}
			}
		}
	}
	fmt.Printf("sink %d\n", sink)
}
