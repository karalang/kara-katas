// Benchmark for #487: Rust mirror of the ★ arm (the run before the
// last 0); see max_consecutive_ones_ii.kara.

fn find_max_consecutive_ones(nums: &[i64]) -> i64 {
    let mut best = 0;
    let mut before = 0;
    let mut run = 0;
    for &x in nums {
        if x == 1 {
            run += 1;
        } else {
            before = run + 1;
            run = 0;
        }
        if before + run > best {
            best = before + run;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut seed: i64 = 487;
    for a in 0..20 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums.push(if next_random(&mut seed) % 100 < 80 + a { 1 } else { 0 });
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for nums in &arrays {
            let best = find_max_consecutive_ones(nums);
            total += best;
            checksum = (checksum * 31 + best) % 1000000007;
        }
    }
    println!("1000 scans of 100000 numbers: runs add up to {total}, checksum {checksum}");
}
