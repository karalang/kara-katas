// LeetCode #706 bench: the ★ arm in Go. See the .kara twin for the
// workload.
package main

import "fmt"

type pair struct {
	key   int64
	value int64
}

type MyHashMap struct {
	buckets [][]pair
}

func newMyHashMap() *MyHashMap {
	return &MyHashMap{buckets: make([][]pair, 1009)}
}

func (m *MyHashMap) put(key, value int64) {
	b := key % 1009
	for i := range m.buckets[b] {
		if m.buckets[b][i].key == key {
			m.buckets[b][i] = pair{key, value}
			return
		}
	}
	m.buckets[b] = append(m.buckets[b], pair{key, value})
}

func (m *MyHashMap) get(key int64) int64 {
	for _, p := range m.buckets[key%1009] {
		if p.key == key {
			return p.value
		}
	}
	return -1
}

func (m *MyHashMap) remove(key int64) {
	b := key % 1009
	pairs := m.buckets[b]
	for i := range pairs {
		if pairs[i].key == key {
			pairs[i] = pairs[len(pairs)-1]
			m.buckets[b] = pairs[:len(pairs)-1]
			return
		}
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(706)
	found := 0
	checksum := int64(0)
	for round := 0; round < 5; round++ {
		for mapNo := 0; mapNo < 10; mapNo++ {
			m := newMyHashMap()
			for i := 0; i < 300000; i++ {
				op := nextRandom(&seed) % 3
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				key := (hi*32768 + lo) % 50000
				if op == 0 {
					vhi := nextRandom(&seed)
					vlo := nextRandom(&seed)
					m.put(key, (vhi*32768+vlo)%1000000)
				} else if op == 1 {
					value := m.get(key)
					if value >= 0 {
						found++
					}
					checksum = (checksum*31 + value + 1) % 1000000007
				} else {
					m.remove(key)
				}
			}
		}
	}
	fmt.Printf("5 rounds of 10 maps of 300000 calls: %d found, checksum %d\n", found, checksum)
}
