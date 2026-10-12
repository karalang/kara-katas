// Benchmark for #379: mirror of phone_directory.kara.

struct PhoneDirectory {
    size: usize,
    free: Vec<i64>,
}

impl PhoneDirectory {
    fn new(max_numbers: usize) -> PhoneDirectory {
        let mut size = 1;
        while size < max_numbers {
            size *= 2;
        }
        let mut free = vec![0i64; 2 * size];
        for n in 0..max_numbers {
            free[size + n] = 1;
        }
        for i in (1..size).rev() {
            free[i] = free[2 * i] + free[2 * i + 1];
        }
        PhoneDirectory { size, free }
    }

    fn set(&mut self, number: usize, value: i64) {
        let mut i = self.size + number;
        self.free[i] = value;
        i /= 2;
        while i >= 1 {
            self.free[i] = self.free[2 * i] + self.free[2 * i + 1];
            i /= 2;
        }
    }

    fn get(&mut self) -> i64 {
        if self.free[1] == 0 {
            return -1;
        }
        let mut i = 1;
        while i < self.size {
            i = if self.free[2 * i] > 0 { 2 * i } else { 2 * i + 1 };
        }
        let number = i - self.size;
        self.set(number, 0);
        number as i64
    }

    fn check(&self, number: usize) -> bool {
        self.free[self.size + number] == 1
    }

    fn release(&mut self, number: usize) {
        self.set(number, 1);
    }
}

fn main() {
    let m: i64 = 10000;
    let mut dir = PhoneDirectory::new(m as usize);
    let mut seed: i64 = 379;
    let mut checksum: i64 = 0;
    for _ in 0..20000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let op = (seed / 65536) % 4;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let x = ((seed / 65536) % m) as usize;
        let v = if op == 0 {
            dir.get() + 1
        } else if op == 1 {
            if dir.check(x) { 1 } else { 0 }
        } else {
            dir.release(x);
            0
        };
        checksum = (checksum * 31 + v) % 1000000007;
    }
    println!("checksum {}", checksum);
}
