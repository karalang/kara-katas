// LeetCode #1656: Design an Ordered Stream -- the bench's Go mirror: the ★
// arm on 2000 random streams of 1000 pairs, each inserted in a random
// order with a value of five random letters, all drawn first.
package main

import "fmt"

type OrderedStream struct {
	slots []*string
	next  int
}

func NewOrderedStream(n int32) *OrderedStream {
	return &OrderedStream{slots: make([]*string, n+1), next: 1}
}

func (s *OrderedStream) Insert(idKey int32, value string) []string {
	s.slots[idKey] = &value
	chunk := []string{}
	for s.next < len(s.slots) && s.slots[s.next] != nil {
		chunk = append(chunk, *s.slots[s.next])
		s.next++
	}
	return chunk
}

var seed int64 = 1656

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type pair struct {
	id    int32
	value string
}

func main() {
	const n = 1000
	streams := make([][]pair, 0, 2000)
	for s := 0; s < 2000; s++ {
		order := make([]int32, n)
		for i := range order {
			order[i] = int32(i + 1)
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			order[i], order[j] = order[j], order[i]
		}
		pairs := make([]pair, 0, n)
		for _, id := range order {
			b := make([]byte, 5)
			for c := range b {
				b[c] = byte('a' + nextRandom()%26)
			}
			pairs = append(pairs, pair{id, string(b)})
		}
		streams = append(streams, pairs)
	}
	var check, chunks int64
	for _, pairs := range streams {
		stream := NewOrderedStream(n)
		for _, p := range pairs {
			chunk := stream.Insert(p.id, p.value)
			if len(chunk) > 0 {
				chunks++
			}
			for _, v := range chunk {
				for i := 0; i < len(v); i++ {
					check = (check*31 + int64(v[i])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("2000 streams of 1000 pairs: %d chunks, checksum %d\n", chunks, check)
}
