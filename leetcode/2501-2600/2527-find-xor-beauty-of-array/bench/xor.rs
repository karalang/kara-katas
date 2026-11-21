// LeetCode #2527: Find Xor-Beauty of Array -- Rust mirror of the benchmark
// (xor.kara): the same lists, passes, order and checksum.

fn xor_beauty(nums: &[i64]) -> i64 {
    let mut beauty = 0;
    for &x in nums.iter() {
        beauty ^= x;
    }
    beauty
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2527;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        lists.push((0..100).map(|_| wide_random(&mut seed) % 1000000000 + 1).collect());
    }
    let passes = 3000;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 1000;
        for i in 0..1000 {
            check = (check * 31 + xor_beauty(&lists[((start + i) % 1000) as usize]) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 1000 lists of 100 numbers: checksum {check}");
}
