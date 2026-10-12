// Benchmark for #458: mirror of poor_pigs.kara (the ★ arm, growing the
// number of outcomes) on the same workload.
package main

import "fmt"

func poorPigs(buckets, minutesToDie, minutesToTest int64) int64 {
	states := minutesToTest/minutesToDie + 1
	pigs := int64(0)
	covered := int64(1)
	for covered < buckets {
		covered *= states
		pigs++
	}
	return pigs
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n int64 = 1000000
	const rounds = 20
	seed := int64(458)
	buckets := make([]int64, 0, n)
	die := make([]int64, 0, n)
	test := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		digits := nextRandom(&seed) % 13
		top := int64(1)
		for j := int64(0); j < digits; j++ {
			top *= 10
		}
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		c := nextRandom(&seed)
		r := (a*65536+b)*65536 + c
		buckets = append(buckets, 1+r%top)
		d := 1 + nextRandom(&seed)%100
		die = append(die, d)
		test = append(test, d+nextRandom(&seed)%(101-d))
	}
	total := int64(0)
	checksum := int64(0)
	for round := 0; round < rounds; round++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		k := (hi*65536 + lo) % n
		hi = nextRandom(&seed)
		lo = nextRandom(&seed)
		buckets[k] = 1 + (hi*65536+lo)%1000000000000
		sum := int64(0)
		for i := int64(0); i < n; i++ {
			sum += poorPigs(buckets[i], die[i], test[i])
		}
		total += sum
		checksum = (checksum*31 + sum) % 1000000007
	}
	fmt.Printf("%d rounds on %d queries: %d pigs, checksum %d\n", rounds, n, total, checksum)
}
