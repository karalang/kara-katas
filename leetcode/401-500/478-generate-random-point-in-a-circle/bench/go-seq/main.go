// Benchmark for #478: Go mirror of the ★ arm (darts at the square); see
// ../random_point.kara.
package main

import "fmt"

type Uniform struct {
	seed int64
}

func (u *Uniform) step() int64 {
	u.seed = (u.seed*1103515245 + 12345) % 2147483648
	return u.seed / 65536
}

func (u *Uniform) next() float64 {
	high := u.step()
	low := u.step()
	return float64(high*32768+low) / 1073741824.0
}

type Solution struct {
	radius, xCenter, yCenter float64
	rng                      Uniform
}

func (s *Solution) randPoint() (float64, float64) {
	for {
		x := 2.0*s.rng.next() - 1.0
		y := 2.0*s.rng.next() - 1.0
		if x*x+y*y <= 1.0 {
			return s.xCenter + s.radius*x, s.yCenter + s.radius*y
		}
	}
}

func main() {
	n := 20000000
	solution := Solution{10000.0, 20000.0, 30000.0, Uniform{478}}
	var right, checksum int64
	for i := 0; i < n; i++ {
		x, y := solution.randPoint()
		if x > 20000.0 {
			right++
		}
		checksum = (checksum*31 + int64(x*1000.0) + int64(y*1000.0)) % 1000000007
	}
	fmt.Printf("%d points: %d right of the centre, checksum %d\n", n, right, checksum)
}
