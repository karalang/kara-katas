// LeetCode #1603: Design Parking System -- the bench in Go, mirroring
// parking.kara: the spaces left of each size in a slice.
package main

import "fmt"

type ParkingSystem struct {
	left []int32
}

func newParkingSystem(big, medium, small int32) *ParkingSystem {
	return &ParkingSystem{left: []int32{big, medium, small}}
}

func (p *ParkingSystem) addCar(carType int32) bool {
	slot := carType - 1
	if p.left[slot] == 0 {
		return false
	}
	p.left[slot]--
	return true
}

var seed int64 = 1603

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var lots [1000][3]int32
	for k := range lots {
		for s := 0; s < 3; s++ {
			lots[k][s] = int32(nextRandom() % 3001)
		}
	}
	cars := make([]int32, 10000000)
	for i := range cars {
		cars[i] = int32(nextRandom()%3 + 1)
	}
	var check, parked int64
	for round := int64(0); round < 20; round++ {
		for k := range lots {
			lot := newParkingSystem(lots[k][0], lots[k][1], lots[k][2])
			var count int64
			for _, c := range cars[k*10000 : (k+1)*10000] {
				if lot.addCar(c) {
					count++
				}
			}
			parked += count
			check = (check*31 + count + round + 1) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each: %d parked, checksum %d\n", parked, check)
}
