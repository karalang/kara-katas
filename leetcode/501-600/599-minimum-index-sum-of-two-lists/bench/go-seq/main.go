// Benchmark for #599: Go mirror of the ★ arm (index the first list in a
// map, then walk the second); see ../find_restaurant.kara. Go strings
// are immutable and share their bytes, so the map's keys and the answer
// are not copied, where the Kāra arm clones each one.
package main

import "fmt"

func findRestaurant(list1, list2 []string) []string {
	index := map[string]int{}
	for i, s := range list1 {
		index[s] = i
	}
	best := len(list1) + len(list2)
	answer := []string{}
	for j, s := range list2 {
		if i, ok := index[s]; ok {
			sum := i + j
			if sum < best {
				best = sum
				answer = answer[:0]
			}
			if sum == best {
				answer = append(answer, s)
			}
		}
	}
	return answer
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// spell writes k in lower-case letters, base 26, the last letter the units.
func spell(k int64) string {
	letters := []byte{}
	for {
		letters = append([]byte{byte('a' + k%26)}, letters...)
		k /= 26
		if k == 0 {
			break
		}
	}
	return string(letters)
}

func main() {
	count := 100
	rounds := 100
	seed := int64(599)
	pool := []string{}
	for k := 0; k < 3000; k++ {
		number := step(&seed) * 32768
		number += step(&seed)
		pool = append(pool, fmt.Sprintf("restaurant %s at %s", spell(int64(k)), spell(number)))
	}
	order := make([]int, len(pool))
	for k := range order {
		order[k] = k
	}
	type pair struct{ a, b []string }
	pairs := []pair{}
	for c := 0; c < count; c++ {
		lists := [][]string{}
		for t := 0; t < 2; t++ {
			list := []string{}
			for k := 0; k < 1000; k++ {
				j := k + int(step(&seed)%int64(len(pool)-k))
				order[k], order[j] = order[j], order[k]
				list = append(list, pool[order[k]])
			}
			lists = append(lists, list)
		}
		pairs = append(pairs, pair{lists[0], lists[1]})
	}
	total := 0
	var checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			p := pairs[(round*7+g)%count]
			got := findRestaurant(p.a, p.b)
			total += len(got)
			for _, s := range got {
				checksum = (checksum*31 + int64(len(s))) % 1000000007
				checksum = (checksum*31 + int64(s[len(s)-1])) % 1000000007
			}
		}
	}
	fmt.Printf("%d pairs, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}
