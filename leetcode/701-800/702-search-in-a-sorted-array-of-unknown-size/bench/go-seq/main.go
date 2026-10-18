// LeetCode #702: Search in a Sorted Array of Unknown Size -- bench program, Go mirror of the doubling arm.
package main

import "fmt"

type ArrayReader struct {
	secret []int64
	reads  int64
}

func (r *ArrayReader) get(index int64) int64 {
	r.reads++
	if index < 0 || index >= int64(len(r.secret)) {
		return 2147483647
	}
	return r.secret[index]
}

func search(reader *ArrayReader, target int64) int64 {
	lo, hi := int64(0), int64(1)
	for reader.get(hi) < target {
		lo = hi
		hi *= 2
	}
	for lo <= hi {
		mid := lo + (hi-lo)/2
		v := reader.get(mid)
		if v == target {
			return mid
		}
		if v < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(702)
	readers := make([]ArrayReader, 100)
	for a := range readers {
		secret := make([]int64, 10000)
		v := int64(-10000)
		for i := range secret {
			secret[i] = v
			v += 1 + nextRandom(&seed)%2
		}
		readers[a] = ArrayReader{secret: secret}
	}
	const rounds = 5
	found := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for a := range readers {
			for target := int64(-10000); target <= 10000; target += 2 {
				at := search(&readers[a], target)
				if at >= 0 {
					found++
					checksum = (checksum*31 + at) % 1000000007
				}
			}
		}
	}
	reads := int64(0)
	for a := range readers {
		reads += readers[a].reads
	}
	fmt.Printf("%d rounds of 100 arrays of 10000: %d found, %d reads, checksum %d\n", rounds, found, reads, checksum)
}
