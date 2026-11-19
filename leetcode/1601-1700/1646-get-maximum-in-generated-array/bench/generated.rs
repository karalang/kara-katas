// LeetCode #1646: Get Maximum in Generated Array -- the bench's Rust
// mirror: the ★ arm on 4000000 random n from 0 to 100, all drawn first.

fn get_maximum_generated(n: i32) -> i32 {
    if n == 0 {
        return 0;
    }
    let n = n as usize;
    let mut nums = vec![0i32; n + 1];
    nums[1] = 1;
    let mut best = 1;
    for i in 2..=n {
        nums[i] = if i % 2 == 0 { nums[i / 2] } else { nums[i / 2] + nums[i / 2 + 1] };
        best = best.max(nums[i]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let cases = 4000000;
    let mut seed: i64 = 1646;
    let ns: Vec<i32> = (0..cases).map(|_| (next_random(&mut seed) % 101) as i32).collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &n in &ns {
        let found = get_maximum_generated(n) as i64;
        total += found;
        check = (check * 31 + found + 1) % 1000000007;
    }
    println!("{} random n up to 100: maxima sum to {}, checksum {}", cases, total, check);
}
