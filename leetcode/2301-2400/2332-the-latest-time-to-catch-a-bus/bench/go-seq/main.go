// LeetCode #2332: The Latest Time to Catch a Bus -- the bench, the ★ arm
// in Go. Both lists copied and sorted, the buses fill in order from the
// earliest passengers; the last bus's departure if it leaves with room,
// else its last passenger's time, then a step back past every passenger
// standing at the time tried. O((n + m) log(n + m)).
package main

import (
	"fmt"
	"slices"
)

func latestTimeCatchTheBus(busIn, passIn []int64, capacity int64) int64 {
	buses := slices.Clone(busIn)
	passengers := slices.Clone(passIn)
	slices.Sort(buses)
	slices.Sort(passengers)
	next, aboard := 0, int64(0)
	for _, bus := range buses {
		aboard = 0
		for aboard < capacity && next < len(passengers) && passengers[next] <= bus {
			aboard++
			next++
		}
	}
	var latest int64
	if aboard < capacity {
		latest = buses[len(buses)-1]
	} else {
		latest = passengers[next-1]
	}
	for k := next - 1; k >= 0 && passengers[k] == latest; k-- {
		latest--
	}
	return latest
}

func scrambled(index int64) int64 { return index*2654435761%2147483647 + 2 }

func main() {
	buses := make([][]int64, 10)
	passengers := make([][]int64, 10)
	for k := int64(0); k < 10; k++ {
		base := k * 150000
		buses[k] = make([]int64, 50000)
		for i := range buses[k] {
			buses[k][i] = scrambled(base + int64(i))
		}
		passengers[k] = make([]int64, 100000)
		for i := range passengers[k] {
			passengers[k][i] = scrambled(base + 50000 + int64(i))
		}
	}
	var check int64
	for p := int64(0); p < 5; p++ {
		for k := int64(0); k < 10; k++ {
			check = (check*31 + latestTimeCatchTheBus(buses[k], passengers[k], 1+(k+p)%5)) % 1000000007
		}
	}
	fmt.Printf("5 passes over 10 cases of 5*10^4 buses and 10^5 passengers: checksum %d\n", check)
}
