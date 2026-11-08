// LeetCode #2021: Brightest Position on Street -- the ★ arm's benchmark, a
// mirror of brightest.kara: the events built and sorted per call.
package main

import (
	"fmt"
	"sort"
)

type event struct{ at, delta int64 }

func brightestPosition(lights [][2]int64) int64 {
	events := make([]event, 0, 2*len(lights))
	for _, l := range lights {
		events = append(events, event{l[0] - l[1], 1}, event{l[0] + l[1] + 1, -1})
	}
	sort.Slice(events, func(i, j int) bool {
		if events[i].at != events[j].at {
			return events[i].at < events[j].at
		}
		return events[i].delta < events[j].delta
	})
	var brightness, best, answer int64
	i := 0
	for i < len(events) {
		at := events[i].at
		for i < len(events) && events[i].at == at {
			brightness += events[i].delta
			i++
		}
		if brightness > best {
			best = brightness
			answer = at
		}
	}
	return answer
}

var seed int64 = 2021

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	spreads := []int64{1000000, 10000000, 100000000}
	reaches := []int64{1000, 100000, 1000000}
	streets := make([][][2]int64, 0, 100)
	for s := 0; s < 100; s++ {
		spread, reach := spreads[s%3], reaches[s%3]
		lights := make([][2]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			hi := nextRandom()
			lo := nextRandom()
			position := (hi*32768+lo)%(2*spread+1) - spread
			lights = append(lights, [2]int64{position, nextRandom() % (reach + 1)})
		}
		streets = append(streets, lights)
	}
	var calls, sum, check int64
	for r := 0; r < 5; r++ {
		for _, lights := range streets {
			answer := brightestPosition(lights)
			calls++
			sum += answer
			check = (check*31 + answer + 1000000000) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
