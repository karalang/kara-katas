// LeetCode #2753: Count Houses in a Circular Street II -- the bench in
// Go: the ★ arm over 30 streets of up to 10^5 houses with k = 10^5, all
// drawn first, then each walked 20 times, every walk on a fresh copy of
// its street, the walk closing the doors it meets.
package main

import "fmt"

type Street struct {
	doors []bool
	at    int
	moves int64
}

func (s *Street) closeDoor()       { s.doors[s.at] = false }
func (s *Street) isDoorOpen() bool { return s.doors[s.at] }
func (s *Street) moveRight() {
	s.at = (s.at + 1) % len(s.doors)
	s.moves++
}

func houseCount(street *Street, k int64) int64 {
	for !street.isDoorOpen() {
		street.moveRight()
	}
	var last int64
	for step := int64(1); step <= k; step++ {
		street.moveRight()
		if street.isDoorOpen() {
			street.closeDoor()
			last = step
		}
	}
	return last
}

var seed int64 = 2753

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 30
	rounds := 20
	var k int64 = 100000
	doors := make([][]bool, count)
	starts := make([]int, count)
	for c := 0; c < count; c++ {
		n := nextRandom()%k + 1
		doors[c] = make([]bool, n)
		for i := range doors[c] {
			doors[c][i] = nextRandom()%2 == 0
		}
		doors[c][nextRandom()%n] = true
		starts[c] = int(nextRandom() % n)
	}
	var total, moves, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			street := Street{doors: append([]bool(nil), doors[c]...), at: starts[c]}
			a := houseCount(&street, k)
			total += a
			moves += street.moves
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d streets, %d rounds: houses sum to %d in %d moves, checksum %d\n", count, rounds, total, moves, check)
}
