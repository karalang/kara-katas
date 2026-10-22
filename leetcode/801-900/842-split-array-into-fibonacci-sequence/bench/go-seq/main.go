// Benchmark for #842: Split Array into Fibonacci Sequence -- Go twin of the
// Kāra ★ arm (the first two numbers decide the rest).
package main

import (
	"fmt"
	"strconv"
)

func read(d string, start, length int) int64 {
	if length > 1 && d[start] == '0' {
		return -1
	}
	var value int64
	for k := start; k < start+length; k++ {
		value = value*10 + int64(d[k]-'0')
	}
	if value > 2147483647 {
		return -1
	}
	return value
}

func splitIntoFibonacci(d string) []int64 {
	n := len(d)
	for i := 1; i < 11; i++ {
		for j := 1; j < 11; j++ {
			if i+j >= n {
				break
			}
			a, b := read(d, 0, i), read(d, i, j)
			if a < 0 || b < 0 {
				continue
			}
			seq := []int64{a, b}
			pos := i + j
			for pos < n {
				c := seq[len(seq)-1] + seq[len(seq)-2]
				if c > 2147483647 {
					break
				}
				digits := strconv.FormatInt(c, 10)
				if pos+len(digits) > n {
					break
				}
				if d[pos:pos+len(digits)] != digits {
					break
				}
				seq = append(seq, c)
				pos += len(digits)
			}
			if pos == n {
				return seq
			}
		}
	}
	return nil
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 64, 240000
	seed := int64(842)
	cases := make([]string, 0, count)
	tops := []int64{10, 1000, 100000}
	for g := 0; g < count; g++ {
		top := tops[g%3]
		x := nextRandom(&seed) % top
		y := nextRandom(&seed) % top
		s := strconv.FormatInt(x, 10) + strconv.FormatInt(y, 10)
		for {
			z := x + y
			w := strconv.FormatInt(z, 10)
			if z > 2147483647 || len(s)+len(w) > 200 {
				break
			}
			s += w
			x, y = y, z
		}
		if g%4 == 3 {
			d := []byte(s)
			at := nextRandom(&seed) % int64(len(d))
			d[at] = '0' + (d[at]-'0'+1)%10
			s = string(d)
		}
		cases = append(cases, s)
	}
	split, checksum := int64(0), int64(0)
	for round := 0; round < rounds; round++ {
		seq := splitIntoFibonacci(cases[round%count])
		if len(seq) > 0 {
			split++
			checksum = (checksum*31 + int64(len(seq))*1000 + seq[len(seq)-1]%1000) % 1000000007
		} else {
			checksum = (checksum*31 + 7) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d strings: %d split, checksum %d\n", rounds, count, split, checksum)
}
