// LeetCode #2069: Walking Robot Simulation II -- Go mirror of the ★
// arm's benchmark (robot.kara): 200 robots of 2 to 100 by 2 to 100, 50000
// calls each, half of them steps of up to 100000 cells.
package main

import "fmt"

type Robot struct {
	width, height, at int64
	moved             bool
}

func (r *Robot) step(num int64) {
	r.moved = true
	r.at = (r.at + num) % (2*(r.width+r.height) - 4)
}

func (r *Robot) getPos() []int64 {
	w, h, at := r.width-1, r.height-1, r.at
	if at <= w {
		return []int64{at, 0}
	} else if at <= w+h {
		return []int64{w, at - w}
	} else if at <= 2*w+h {
		return []int64{2*w + h - at, h}
	}
	return []int64{0, 2*w + 2*h - at}
}

func (r *Robot) getDir() string {
	w, h, at := r.width-1, r.height-1, r.at
	if at == 0 {
		if r.moved {
			return "South"
		}
		return "East"
	} else if at <= w {
		return "East"
	} else if at <= w+h {
		return "North"
	} else if at <= 2*w+h {
		return "West"
	}
	return "South"
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2069)
	check := int64(0)
	for t := int64(0); t < 200; t++ {
		robot := &Robot{width: 2 + t%99, height: 2 + t*7%99}
		for k := 0; k < 50000; k++ {
			kind := nextRandom(&seed) % 4
			if kind < 2 {
				a := nextRandom(&seed)
				b := nextRandom(&seed)
				robot.step((a*32768+b)%100000 + 1)
			} else if kind == 2 {
				p := robot.getPos()
				check = (check*31 + p[0]*1000 + p[1]) % 1000000007
			} else {
				check = (check*31 + int64(len(robot.getDir()))) % 1000000007
			}
		}
	}
	fmt.Printf("200 robots, 10000000 calls: checksum %d\n", check)
}
