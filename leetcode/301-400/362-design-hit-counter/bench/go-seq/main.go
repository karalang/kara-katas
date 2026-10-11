// Benchmark for #362 -- mirror of hit_counter.kara.
package main

import "fmt"

// hitCounter keeps the window in a slice used as a queue; the dead prefix is
// dropped by reslicing, and append reuses or grows the backing array.
type hitCounter struct{ hits []int64 }

func (c *hitCounter) hit(timestamp int64) { c.hits = append(c.hits, timestamp) }

func (c *hitCounter) getHits(timestamp int64) int64 {
	for len(c.hits) > 0 && c.hits[0] <= timestamp-300 {
		c.hits = c.hits[1:]
	}
	return int64(len(c.hits))
}

func main() {
	var seed int64 = 362
	c := &hitCounter{}
	var t int64 = 1
	var checksum int64
	for i := 0; i < 2000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		t += (seed / 65536) % 3
		seed = (seed*1103515245 + 12345) % 2147483648
		if (seed/65536)%4 == 0 {
			checksum = (checksum*31 + c.getHits(t)) % 1000000007
		} else {
			c.hit(t)
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
