// Benchmark for #379: mirror of phone_directory.kara.
package main

import "fmt"

type PhoneDirectory struct {
	size int64
	free []int64
}

func newDir(maxNumbers int64) *PhoneDirectory {
	size := int64(1)
	for size < maxNumbers {
		size *= 2
	}
	free := make([]int64, 2*size)
	for n := int64(0); n < maxNumbers; n++ {
		free[size+n] = 1
	}
	for i := size - 1; i >= 1; i-- {
		free[i] = free[2*i] + free[2*i+1]
	}
	return &PhoneDirectory{size, free}
}

func (d *PhoneDirectory) set(number, value int64) {
	i := d.size + number
	d.free[i] = value
	i /= 2
	for i >= 1 {
		d.free[i] = d.free[2*i] + d.free[2*i+1]
		i /= 2
	}
}

func (d *PhoneDirectory) get() int64 {
	if d.free[1] == 0 {
		return -1
	}
	i := int64(1)
	for i < d.size {
		if d.free[2*i] > 0 {
			i = 2 * i
		} else {
			i = 2*i + 1
		}
	}
	number := i - d.size
	d.set(number, 0)
	return number
}

func (d *PhoneDirectory) check(number int64) bool { return d.free[d.size+number] == 1 }

func (d *PhoneDirectory) release(number int64) { d.set(number, 1) }

func main() {
	const m = 10000
	d := newDir(m)
	seed := int64(379)
	checksum := int64(0)
	for q := 0; q < 20000000; q++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		op := (seed / 65536) % 4
		seed = (seed*1103515245 + 12345) % 2147483648
		x := (seed / 65536) % m
		var v int64
		switch {
		case op == 0:
			v = d.get() + 1
		case op == 1:
			if d.check(x) {
				v = 1
			}
		default:
			d.release(x)
		}
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
