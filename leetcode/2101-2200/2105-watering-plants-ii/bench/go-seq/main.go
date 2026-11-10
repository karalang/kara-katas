// LeetCode #2105: Watering Plants II -- bench, Go mirror of
// watering.kara.
package main

import "fmt"

func minimumRefill(plants []int64, capacityA, capacityB int64) int64 {
	i, j := 0, len(plants)-1
	a, b := capacityA, capacityB
	var refills int64
	for i < j {
		if a < plants[i] {
			refills++
			a = capacityA
		}
		a -= plants[i]
		if b < plants[j] {
			refills++
			b = capacityB
		}
		b -= plants[j]
		i++
		j--
	}
	if i == j && max(a, b) < plants[i] {
		refills++
	}
	return refills
}

var seed int64 = 2105

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

type row struct {
	plants []int64
	a, b   int64
}

func main() {
	rows := make([]row, 0, 200)
	for r := 0; r < 200; r++ {
		plants := make([]int64, 100000)
		var most int64
		for k := range plants {
			plants[k] = wideRandom()%1000000 + 1
			if plants[k] > most {
				most = plants[k]
			}
		}
		a := most + wideRandom()%(2000000-most+1)
		b := most + wideRandom()%(2000000-most+1)
		rows = append(rows, row{plants, a, b})
	}
	var total, check int64
	for p := 0; p < 10; p++ {
		for _, r := range rows {
			got := minimumRefill(r.plants, r.a, r.b)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("2000 rows: %d refills, checksum %d\n", total, check)
}
