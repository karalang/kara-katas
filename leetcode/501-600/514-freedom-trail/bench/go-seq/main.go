// Benchmark for #514: Go mirror of the ★ arm (a cost per position of the
// current letter); see ../find_rotate_steps.kara.
package main

import "fmt"

func findRotateSteps(ring []byte, key []byte) int64 {
	n := int64(len(ring))
	at := make([][]int64, 26)
	for j := range ring {
		at[ring[j]-'a'] = append(at[ring[j]-'a'], int64(j))
	}
	prevPos := []int64{0}
	prevCost := []int64{0}
	for _, c := range key {
		pos := append([]int64(nil), at[c-'a']...)
		var cost []int64
		for _, q := range pos {
			best := int64(1<<63 - 1)
			for i := range prevPos {
				d := prevPos[i] - q
				if d < 0 {
					d = -d
				}
				if n-d < d {
					d = n - d
				}
				if prevCost[i]+d < best {
					best = prevCost[i] + d
				}
			}
			cost = append(cost, best)
		}
		prevPos = pos
		prevCost = cost
	}
	fewest := int64(1<<63 - 1)
	for _, c := range prevCost {
		if c < fewest {
			fewest = c
		}
	}
	return fewest + int64(len(key))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 400 random rings of 300 letters from all 26, each with a key of
	// 2,000 letters drawn from the ring, solved once each.
	seed := int64(514)
	rings := 400
	var total, checksum int64
	for t := 0; t < rings; t++ {
		ring := make([]byte, 0)
		for i := 0; i < 300; i++ {
			ring = append(ring, byte('a'+nextRandom(&seed)%26))
		}
		key := make([]byte, 0)
		for i := 0; i < 2000; i++ {
			key = append(key, ring[nextRandom(&seed)%300])
		}
		steps := findRotateSteps(ring, key)
		total += steps
		checksum = (checksum*31 + steps) % 1000000007
	}
	fmt.Printf("%d rings of 300 letters, keys of 2000: %d steps in all, checksum %d\n", rings, total, checksum)
}
