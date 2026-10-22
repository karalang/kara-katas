// Benchmark for #846: Hand of Straights -- Go twin of the Kāra open-groups
// arm (sorted runs and a queue of open groups).
package main

import (
	"fmt"
	"slices"
)

func isNStraightHand(hand []int64, groupSize int64) bool {
	if int64(len(hand))%groupSize != 0 {
		return false
	}
	cards := slices.Clone(hand)
	slices.Sort(cards)
	// `started` is a ring buffer of at most groupSize entries
	started := make([]int64, groupSize)
	var head, size int64
	var open, last int64
	i := 0
	for i < len(cards) {
		value := cards[i]
		var count int64
		for i < len(cards) && cards[i] == value {
			count++
			i++
		}
		if open > 0 && (value != last+1 || count < open) {
			return false
		}
		started[(head+size)%groupSize] = count - open
		size++
		last = value
		open = count
		if size == groupSize {
			open -= started[head]
			head = (head + 1) % groupSize
			size--
		}
	}
	return open == 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 3000, 10000
	sizes := []int64{1, 2, 4, 5, 10, 16, 100, 1000}
	var seed int64 = 846
	hands := make([][]int64, 0, count)
	groupSizes := make([]int64, 0, count)
	for g := 0; g < count; g++ {
		groupSize := sizes[g%8]
		window := 1 + nextRandom(&seed)%20000
		hand := make([]int64, 0, n)
		for len(hand) < n {
			start := 999000000 + nextRandom(&seed)%window
			for j := int64(0); j < groupSize; j++ {
				hand = append(hand, start+j)
			}
		}
		for i := 0; i < n; i++ {
			j := i + int(nextRandom(&seed)%int64(n-i))
			hand[i], hand[j] = hand[j], hand[i]
		}
		if g%4 == 3 {
			at := nextRandom(&seed) % n
			hand[at]++
		}
		hands = append(hands, hand)
		groupSizes = append(groupSizes, groupSize)
	}
	splits := 0
	var checksum int64
	for round := 0; round < rounds; round++ {
		ok := isNStraightHand(hands[round%count], groupSizes[round%count])
		if ok {
			splits++
		}
		b := int64(0)
		if ok {
			b = 1
		}
		checksum = (checksum*31 + int64(round%count) + b) % 1000000007
	}
	fmt.Printf("%d rounds of %d hands: %d split, checksum %d\n", rounds, count, splits, checksum)
}
