// Benchmark for #677: the keys kept sorted, as the Kara sorted arm.
package main

import (
	"fmt"
	"strings"
)

type MapSum struct {
	keys []string
	vals []int64
}

func lowerBound(keys []string, word string) int {
	lo, hi := 0, len(keys)
	for lo < hi {
		mid := (lo + hi) / 2
		if keys[mid] < word {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func (m *MapSum) insert(key string, val int64) {
	at := lowerBound(m.keys, key)
	if at < len(m.keys) && m.keys[at] == key {
		m.vals[at] = val
		return
	}
	m.keys = append(m.keys, "")
	copy(m.keys[at+1:], m.keys[at:])
	m.keys[at] = key
	m.vals = append(m.vals, 0)
	copy(m.vals[at+1:], m.vals[at:])
	m.vals[at] = val
}

func (m *MapSum) sum(prefix string) int64 {
	var total int64
	for i := lowerBound(m.keys, prefix); i < len(m.keys) && strings.HasPrefix(m.keys[i], prefix); i++ {
		total += m.vals[i]
	}
	return total
}

var seed int64 = 677

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(most int64) string {
	n := 1 + nextRandom()%most
	b := make([]byte, 0, n)
	for i := int64(0); i < n; i++ {
		b = append(b, byte(97+nextRandom()%3))
	}
	return string(b)
}

func main() {
	rounds := 100
	calls := 2000
	var s int64
	for r := 0; r < rounds; r++ {
		m := &MapSum{}
		for k := 0; k < calls; k++ {
			key := randomWord(12)
			m.insert(key, 1+nextRandom()%1000)
		}
		for k := 0; k < calls; k++ {
			s = (s*31 + m.sum(randomWord(3))) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d inserts and %d sums: checksum %d\n", rounds, calls, calls, s)
}
