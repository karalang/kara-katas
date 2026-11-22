// LeetCode #2728: Count Houses in a Circular Street -- the bench in Go:
// the ★ arm over 300 streets of up to 1000 houses with k = 1000, all
// drawn first, then each walked 500 times through the judge's street,
// whose moves are counted.
package main

import "fmt"

type Street struct {
	doors []bool
	at    int
	moves int64
}

func (s *Street) openDoor()        { s.doors[s.at] = true }
func (s *Street) closeDoor()       { s.doors[s.at] = false }
func (s *Street) isDoorOpen() bool { return s.doors[s.at] }
func (s *Street) moveRight() {
	s.at = (s.at + 1) % len(s.doors)
	s.moves++
}

func houseCount(street *Street, k int64) int64 {
	for i := int64(0); i < k; i++ {
		street.closeDoor()
		street.moveRight()
	}
	street.openDoor()
	var houses int64 = 1
	street.moveRight()
	for !street.isDoorOpen() {
		houses++
		street.moveRight()
	}
	return houses
}

var seed int64 = 2728

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 300
	rounds := 500
	streets := make([]Street, count)
	for c := 0; c < count; c++ {
		n := nextRandom()%1000 + 1
		streets[c].doors = make([]bool, n)
		for i := range streets[c].doors {
			streets[c].doors[i] = nextRandom()%2 == 0
		}
		streets[c].at = int(nextRandom() % n)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := houseCount(&streets[c], 1000)
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	var moves int64
	for c := 0; c < count; c++ {
		moves += streets[c].moves
	}
	fmt.Printf("%d streets, %d rounds: houses sum to %d in %d moves, checksum %d\n", count, rounds, total, moves, check)
}
