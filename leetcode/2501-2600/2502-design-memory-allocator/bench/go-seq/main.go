// LeetCode #2502: Design Memory Allocator -- Go mirror of the benchmark
// (alloc.kara): the same sessions, calls and checksum; every unit's owner
// in a slice.
package main

import "fmt"

var seed int64 = 2502

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type Allocator struct {
	memory []int64
}

func (a *Allocator) allocate(size, mID int64) int64 {
	var run int64
	for i := range a.memory {
		if a.memory[i] == 0 {
			run++
			if run == size {
				start := int64(i) + 1 - size
				for j := start; j <= int64(i); j++ {
					a.memory[j] = mID
				}
				return start
			}
		} else {
			run = 0
		}
	}
	return -1
}

func (a *Allocator) freeMemory(mID int64) int64 {
	var freed int64
	for i := range a.memory {
		if a.memory[i] == mID {
			a.memory[i] = 0
			freed++
		}
	}
	return freed
}

func main() {
	const sessions = 400
	var check int64
	for s := int64(0); s < sessions; s++ {
		a := &Allocator{memory: make([]int64, 1000)}
		for k := 0; k < 1000; k++ {
			var r int64
			if (nextRandom()+check)%3 < 2 {
				size := nextRandom()%20 + 1
				r = a.allocate(size, nextRandom()%50+1)
			} else {
				r = a.freeMemory(nextRandom()%50 + 1)
			}
			check = (check*31 + r + 1 + s) % 1000000007
		}
	}
	fmt.Printf("%d sessions of 1000 calls on 1000 units: checksum %d\n", sessions, check)
}
