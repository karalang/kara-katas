// Benchmark for #553: Rust mirror of the ★ arm (the shape is always the
// same); see optimal_division.kara.

fn optimal_division(nums: &[i64]) -> String {
    let n = nums.len();
    let mut out = String::new();
    for i in 0..n {
        if i > 0 {
            out.push('/');
        }
        if i == 1 && n > 2 {
            out.push('(');
        }
        out.push_str(&format!("{}", nums[i]));
    }
    if n > 2 {
        out.push(')');
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 2000;
    let mut seed: i64 = 553;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let n = 1 + next_random(&mut seed) % 10;
        let mut nums = Vec::new();
        for _ in 0..n {
            nums.push(2 + next_random(&mut seed) % 999);
        }
        all.push(nums);
    }
    let mut chars: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..500 {
        for g in 0..count {
            let text = optimal_division(&all[(round * 7 + g) % count]);
            let b = text.as_bytes();
            chars += b.len() as i64;
            checksum = (checksum * 31 + b.len() as i64 + b[b.len() / 2] as i64) % 1000000007;
        }
    }
    println!("{} arrays, 500 rounds each: {} characters, checksum {}", count, chars, checksum);
}
