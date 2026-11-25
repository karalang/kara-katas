// LeetCode #1352 bench -- Rust: the running products since the last zero,
// after a leading 1.

struct ProductOfNumbers {
    prefix: Vec<i64>,
}

impl ProductOfNumbers {
    fn new() -> Self {
        ProductOfNumbers { prefix: vec![1] }
    }

    fn add(&mut self, num: i32) {
        if num == 0 {
            self.prefix.clear();
            self.prefix.push(1);
        } else {
            let last = *self.prefix.last().unwrap();
            self.prefix.push(last * num as i64);
        }
    }

    fn get_product(&self, k: usize) -> i32 {
        let n = self.prefix.len();
        if k >= n {
            return 0;
        }
        (self.prefix[n - 1] / self.prefix[n - 1 - k]) as i32
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1352;
    let mut since: i64 = 1;
    let mut p = ProductOfNumbers::new();
    let mut check: i64 = 0;
    for r in 0..10000000i64 {
        let mut num: i64 = 1;
        if next_random(&mut seed) % 1000 == 0 {
            num = 0;
            since = 1;
        } else {
            if next_random(&mut seed) % 20 == 0 {
                num = 2 + next_random(&mut seed) % 99;
            }
            if since * num >= 2147483648 {
                num = 1;
            }
            since *= num;
        }
        p.add(num as i32);
        let k = 1 + check % 50000i64.min(r + 1);
        check = (check * 31 + p.get_product(k as usize) as i64 + r) % 1000000007;
    }
    println!("10000000 rounds: checksum {}", check);
}
