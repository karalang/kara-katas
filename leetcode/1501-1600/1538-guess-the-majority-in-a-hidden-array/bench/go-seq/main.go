// LeetCode #1538: Guess the Majority in a Hidden Array -- bench: the ★ arm
// (every bit compared with bit 0, n queries) over 100 readers of 5 to 50000
// bits, built once, each asked 20 times. Go mirror of majority.kara.
package main

import "fmt"

type ArrayReader struct {
	nums  []int64
	calls int64
}

func (r *ArrayReader) query(a, b, c, d int32) int32 {
	r.calls++
	ones := r.nums[a] + r.nums[b] + r.nums[c] + r.nums[d]
	if ones == 0 || ones == 4 {
		return 4
	} else if ones == 2 {
		return 0
	}
	return 2
}

func (r *ArrayReader) length() int32 { return int32(len(r.nums)) }

func guessMajority(reader *ArrayReader) int64 {
	n := reader.length()
	q0123 := reader.query(0, 1, 2, 3)
	q1234 := reader.query(1, 2, 3, 4)
	same := make([]bool, n)
	for i := range same {
		same[i] = true
	}
	same[1] = reader.query(0, 2, 3, 4) == q1234
	same[2] = reader.query(0, 1, 3, 4) == q1234
	same[3] = reader.query(0, 1, 2, 4) == q1234
	same[4] = q1234 == q0123
	for i := int32(5); i < n; i++ {
		same[i] = reader.query(1, 2, 3, i) == q0123
	}
	withZero, other := int64(0), int64(-1)
	for i := int32(0); i < n; i++ {
		if same[i] {
			withZero++
		} else {
			other = int64(i)
		}
	}
	if withZero*2 > int64(n) {
		return 0
	} else if withZero*2 < int64(n) {
		return other
	}
	return -1
}

var seed int64 = 1538

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	readers := make([]*ArrayReader, 0, 100)
	for k := 0; k < 100; k++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%49996 + 5
		chance := nextRandom() % 101
		nums := make([]int64, n)
		for i := range nums {
			if nextRandom()%100 < chance {
				nums[i] = 1
			}
		}
		readers = append(readers, &ArrayReader{nums: nums})
	}
	check := int64(0)
	for p := 0; p < 20; p++ {
		for _, r := range readers {
			check = mix(check, guessMajority(r))
		}
	}
	calls := int64(0)
	for _, r := range readers {
		calls += r.calls
	}
	fmt.Printf("20 passes over 100 readers of up to 50000 bits: checksum %d, %d calls\n", check, calls)
}
