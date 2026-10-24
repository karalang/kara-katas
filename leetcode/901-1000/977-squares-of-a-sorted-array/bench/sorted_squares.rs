// Benchmark: LeetCode #977 Squares of a Sorted Array -- the ★ arm, two
// pointers from the ends, on 20 sorted arrays of 10000 numbers. Mirrors
// sorted_squares.kara, .c, .py and go-seq/.

fn sorted_squares(nums: &[i64]) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut out = vec![0; n as usize];
    let mut lo: i64 = 0;
    let mut hi: i64 = n - 1;
    let mut at: i64 = n - 1;
    while lo <= hi {
        let a = nums[lo as usize] * nums[lo as usize];
        let b = nums[hi as usize] * nums[hi as usize];
        if a > b {
            out[at as usize] = a;
            lo += 1;
        } else {
            out[at as usize] = b;
            hi -= 1;
        }
        at -= 1;
    }
    out
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 500;
    let count = 20;
    let n = 10000;
    let mut rng = Rng(977);
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = (0..n).map(|_| rng.next() % 20001 - 10000).collect();
        nums.sort();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let out = sorted_squares(&arrays[(r + i) % count]);
            total += out[0] + out[n - 1];
            check = (check * 31 + out[(r * 13 + i * 7) % n]) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of 10000 numbers: squares total {total}, checksum {check}");
}
