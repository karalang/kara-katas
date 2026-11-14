// LeetCode #1533: Find the Index of the Large Integer -- bench: the ★ arm
// (ternary search) over 100 readers of 2 to 100000 values, built once, each
// searched 20000 times. Go mirror of index.kara.
package main

import "fmt"

type ArrayReader struct {
	sums  []int64
	calls int64
}

func newReader(values []int64) *ArrayReader {
	sums := make([]int64, len(values)+1)
	for i, v := range values {
		sums[i+1] = sums[i] + v
	}
	return &ArrayReader{sums: sums}
}

func (r *ArrayReader) compareSub(l, rr, x, y int32) int32 {
	r.calls++
	left := r.sums[rr+1] - r.sums[l]
	right := r.sums[y+1] - r.sums[x]
	if left > right {
		return 1
	} else if left < right {
		return -1
	}
	return 0
}

func (r *ArrayReader) length() int32 { return int32(len(r.sums) - 1) }

func getIndex(reader *ArrayReader) int64 {
	lo, hi := int32(0), reader.length()-1
	for lo < hi {
		third := (hi - lo + 1) / 3
		if third == 0 {
			if reader.compareSub(lo, lo, hi, hi) > 0 {
				return int64(lo)
			}
			return int64(hi)
		}
		second := lo + third
		switch reader.compareSub(lo, second-1, second, second+third-1) {
		case 1:
			hi = second - 1
		case -1:
			lo = second
			hi = second + third - 1
		default:
			lo = second + third
		}
	}
	return int64(lo)
}

var seed int64 = 1533

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	readers := make([]*ArrayReader, 0, 100)
	for k := 0; k < 100; k++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%99999 + 2
		base := nextRandom()%99 + 1
		large := base + nextRandom()%(100-base) + 1
		b := nextRandom()
		at := (b*32768 + nextRandom()) % n
		values := make([]int64, n)
		for i := range values {
			values[i] = base
		}
		values[at] = large
		readers = append(readers, newReader(values))
	}
	var check int64
	for p := 0; p < 20000; p++ {
		for _, r := range readers {
			check = mix(check, getIndex(r))
		}
	}
	var calls int64
	for _, r := range readers {
		calls += r.calls
	}
	fmt.Printf("20000 passes over 100 readers of up to 100000 values: checksum %d, %d calls\n", check, calls)
}
