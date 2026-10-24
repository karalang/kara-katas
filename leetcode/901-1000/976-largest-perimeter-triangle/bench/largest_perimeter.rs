// Benchmark: LeetCode #976 Largest Perimeter Triangle -- the ★ arm, sort
// and scan from the top, on 20 lists of 10000 random lengths. Mirrors
// largest_perimeter.kara, .c, .py and go-seq/.

fn largest_perimeter(nums: &[i64]) -> i64 {
    let mut a = nums.to_vec();
    a.sort();
    let mut i = a.len() - 1;
    while i >= 2 {
        if a[i - 2] + a[i - 1] > a[i] {
            return a[i - 2] + a[i - 1] + a[i];
        }
        i -= 1;
    }
    0
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 50;
    let count = 20;
    let mut rng = Rng(976);
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums = Vec::with_capacity(10000);
        for _ in 0..10000 {
            let hi = rng.next();
            nums.push(1 + (hi * 32768 + rng.next()) % 1000000);
        }
        lists.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let p = largest_perimeter(&lists[(r + i) % count]);
            total += p;
            check = (check * 31 + p) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} lists of 10000 lengths: perimeters total {total}, checksum {check}");
}
