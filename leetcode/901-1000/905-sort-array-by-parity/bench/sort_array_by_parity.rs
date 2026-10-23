// LeetCode #905: Sort Array By Parity -- bench program, Rust.
//
// The two pointers from both ends, over 1,000,000 numbers below 5001 built
// once. Each round sorts a copy by parity, folds the evens in front and
// one number of the answer into a checksum and changes one number.

fn sort_array_by_parity(nums: Vec<i64>) -> Vec<i64> {
    let mut out = nums;
    let mut i = 0;
    let mut j = out.len() - 1;
    while i < j {
        if out[i] % 2 == 0 {
            i += 1;
        } else if out[j] % 2 == 1 {
            j -= 1;
        } else {
            out.swap(i, j);
            i += 1;
            j -= 1;
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 1000000;
    let rounds: i64 = 100;
    let mut seed: i64 = 905;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(next_random(&mut seed) % 5001);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for round in 0..rounds {
        let out = sort_array_by_parity(nums.clone());
        let mut lead = 0;
        while out[lead] % 2 == 0 {
            lead += 1;
        }
        total += lead as i64;
        check = (check * 31 + lead as i64) % 1000000007;
        check = (check * 31 + out[(round as usize) * 7919 % n]) % 1000000007;
        nums[(round as usize) * 7919 % n] = next_random(&mut seed) % 5001;
    }
    println!("{} rounds over {} numbers: {} evens in front, checksum {}", rounds, n, total, check);
}
