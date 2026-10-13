// Benchmark for #470: mirror of rand10.kara (the ★ arm: rejection
// sampling) on the same workload, over the same seeded rand7.

struct Rand7 {
    seed: i64,
}

impl Rand7 {
    fn rand7(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        1 + (self.seed / 65536) % 7
    }
}

fn rand10(rng: &mut Rand7) -> i64 {
    loop {
        let v = (rng.rand7() - 1) * 7 + rng.rand7();
        if v <= 40 {
            return 1 + (v - 1) % 10;
        }
    }
}

fn main() {
    let n = 20000000;
    let mut rng = Rand7 { seed: 470 };
    let mut counts = vec![0i64; 11];
    let mut checksum: i64 = 0;
    for _ in 0..n {
        let value = rand10(&mut rng);
        counts[value as usize] += 1;
        checksum = (checksum * 11 + value) % 1000000007;
    }
    println!("{n} draws: {} ones, {} tens, checksum {checksum}", counts[1], counts[10]);
}
