// Benchmark for #841: Keys and Rooms -- the ★ arm (a stack of rooms to open).
//
// Mirrors keys_and_rooms.kara: room 0 is open; every room opened is put
// on a stack, and a room taken off the stack gives up its keys, each key
// to a room not yet opened opening it.
package main

import "fmt"

func canVisitAllRooms(rooms [][]int64) bool {
	n := int64(len(rooms))
	opened := make([]bool, n)
	opened[0] = true
	count := int64(1)
	stack := []int64{0}
	for len(stack) > 0 {
		room := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		for _, key := range rooms[room] {
			if !opened[key] {
				opened[key] = true
				count++
				stack = append(stack, key)
			}
		}
	}
	return count == n
}

func contains(v []int64, x int64) bool {
	for _, y := range v {
		if y == x {
			return true
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 64 cases drawn once, each LeetCode's most rooms, 1000: case g puts
	// 2000 keys, each to a random room, in random rooms, no room holding
	// two keys to the same room; when g is even it then threads the
	// rooms in a shuffled order, each holding a key to the next, so that
	// every room can be visited. Each round asks the next case.
	const count, rounds, n = 64, 36000, 1000
	seed := int64(841)
	cases := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		rooms := make([][]int64, n)
		for k := 0; k < 2000; k++ {
			from := nextRandom(&seed) % n
			to := nextRandom(&seed) % n
			if !contains(rooms[from], to) {
				rooms[from] = append(rooms[from], to)
			}
		}
		if g%2 == 0 {
			order := make([]int64, n)
			for i := range order {
				order[i] = int64(i)
			}
			for i := int64(n - 1); i >= 2; i-- {
				j := 1 + nextRandom(&seed)%i
				order[i], order[j] = order[j], order[i]
			}
			for i := 0; i < n-1; i++ {
				if !contains(rooms[order[i]], order[i+1]) {
					rooms[order[i]] = append(rooms[order[i]], order[i+1])
				}
			}
		}
		cases = append(cases, rooms)
	}
	yes, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		all := canVisitAllRooms(cases[round%count])
		v := int64(7)
		if all {
			yes++
			v = round % 1000
		}
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("%d rounds of %d cases: %d with every room visited, checksum %d\n", rounds, count, yes, checksum)
}
