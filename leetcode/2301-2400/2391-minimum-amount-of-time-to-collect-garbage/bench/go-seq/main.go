// LeetCode #2391: Minimum Amount of Time to Collect Garbage -- the bench,
// the ★ arm in Go: the units counted once, each truck driven to the last
// house holding its kind by the travel's prefix sums.
package main

import "fmt"

var seed int64 = 2391

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func garbageCollection(garbage []string, travel []int64) int64 {
	var minutes int64
	last := [3]int{}
	for i, house := range garbage {
		for j := 0; j < len(house); j++ {
			minutes++
			switch house[j] {
			case 'M':
				last[0] = i
			case 'P':
				last[1] = i
			default:
				last[2] = i
			}
		}
	}
	prefix := []int64{0}
	for _, t := range travel {
		prefix = append(prefix, prefix[len(prefix)-1]+t)
	}
	for kind := 0; kind < 3; kind++ {
		minutes += prefix[last[kind]]
	}
	return minutes
}

func main() {
	streets := make([][]string, 50)
	roads := make([][]int64, 50)
	for s := 0; s < 50; s++ {
		street := make([]string, 2000)
		for h := range street {
			length := 1 + nextRandom()%10
			b := make([]byte, length)
			for j := range b {
				b[j] = "MPG"[nextRandom()%3]
			}
			street[h] = string(b)
		}
		streets[s] = street
		road := make([]int64, 1999)
		for h := range road {
			road[h] = 1 + nextRandom()%100
		}
		roads[s] = road
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for s := 0; s < 50; s++ {
			check = (check*31 + garbageCollection(streets[s], roads[s]) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 50 streets of 2000 houses: checksum %d\n", check)
}
