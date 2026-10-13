// Benchmark for #478: Rust mirror of the ★ arm (darts at the square); see
// random_point.kara.

struct Uniform {
    seed: i64,
}

impl Uniform {
    fn new(seed: i64) -> Uniform {
        Uniform { seed }
    }

    fn step(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        self.seed / 65536
    }

    fn next(&mut self) -> f64 {
        let high = self.step();
        let low = self.step();
        (high * 32768 + low) as f64 / 1073741824.0
    }
}

struct Solution {
    radius: f64,
    x_center: f64,
    y_center: f64,
    rng: Uniform,
}

impl Solution {
    fn new(radius: f64, x_center: f64, y_center: f64, seed: i64) -> Solution {
        Solution { radius, x_center, y_center, rng: Uniform::new(seed) }
    }

    fn rand_point(&mut self) -> (f64, f64) {
        loop {
            let x = 2.0 * self.rng.next() - 1.0;
            let y = 2.0 * self.rng.next() - 1.0;
            if x * x + y * y <= 1.0 {
                return (self.x_center + self.radius * x, self.y_center + self.radius * y);
            }
        }
    }
}

fn main() {
    let n = 20000000;
    let mut solution = Solution::new(10000.0, 20000.0, 30000.0, 478);
    let mut right = 0;
    let mut checksum: i64 = 0;
    for _ in 0..n {
        let (x, y) = solution.rand_point();
        if x > 20000.0 {
            right += 1;
        }
        checksum = (checksum * 31 + (x * 1000.0) as i64 + (y * 1000.0) as i64) % 1000000007;
    }
    println!("{} points: {} right of the centre, checksum {}", n, right, checksum);
}
