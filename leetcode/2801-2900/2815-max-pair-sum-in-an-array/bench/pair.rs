// LeetCode #2815: Max Pair Sum in an Array -- the bench in Rust: the ★
// arm over 20000 arrays of 100 numbers up to 10^4, all drawn first, then
// each answered 10 times.

fn largest_digit(x: i64) -> i64 {
    let mut rest = x;
    let mut top = 0;
    while rest > 0 {
        top = top.max(rest % 10);
        rest /= 10;
    }
    top
}

fn max_sum(nums: &[i64]) -> i64 {
    let mut best = [0i64; 10];
    let mut answer = -1;
    for &x in nums {
        let d = largest_digit(x) as usize;
        if best[d] > 0 {
            answer = answer.max(best[d] + x);
        }
        best[d] = best[d].max(x);
    }
    answer
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 20000;
    let rounds = 10;
    let mut rng = Rng(2815);
    let arrays: Vec<Vec<i64>> = (0..count).map(|_| (0..100).map(|_| rng.next_random() % 10000 + 1).collect()).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &arrays {
            let a = max_sum(nums);
            total += a;
            check = (check * 31 + a + 2 + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100, {rounds} rounds: sums total {total}, checksum {check}");
}
