// LeetCode #705 bench: the ★ arm in Go. See the .kara twin for the
// workload.
package main

import "fmt"

type MyHashSet struct {
	buckets [][]int64
}

func newMyHashSet() *MyHashSet {
	return &MyHashSet{buckets: make([][]int64, 1009)}
}

func (s *MyHashSet) has(b int64, key int64) bool {
	for _, k := range s.buckets[b] {
		if k == key {
			return true
		}
	}
	return false
}

func (s *MyHashSet) add(key int64) {
	b := key % 1009
	if !s.has(b, key) {
		s.buckets[b] = append(s.buckets[b], key)
	}
}

func (s *MyHashSet) remove(key int64) {
	b := key % 1009
	keys := s.buckets[b]
	for i, k := range keys {
		if k == key {
			keys[i] = keys[len(keys)-1]
			s.buckets[b] = keys[:len(keys)-1]
			return
		}
	}
}

func (s *MyHashSet) contains(key int64) bool {
	return s.has(key%1009, key)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(705)
	found := 0
	checksum := int64(0)
	for round := 0; round < 5; round++ {
		for setNo := 0; setNo < 10; setNo++ {
			set := newMyHashSet()
			for i := 0; i < 300000; i++ {
				op := nextRandom(&seed) % 3
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				key := (hi*32768 + lo) % 50000
				if op == 0 {
					set.add(key)
				} else if op == 1 {
					set.remove(key)
				} else {
					yes := set.contains(key)
					v := int64(2)
					if yes {
						found++
						v = 1
					}
					checksum = (checksum*3 + v) % 1000000007
				}
			}
		}
	}
	fmt.Printf("5 rounds of 10 sets of 300000 calls: %d found, checksum %d\n", found, checksum)
}
