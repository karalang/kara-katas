// LeetCode #2148: Count Elements With Strictly Smaller and Greater
// Elements -- the benchmark's Rust mirror of elements.kara.

fn count_elements(nums: &[i64]) -> i64 {
    let low = *nums.iter().min().unwrap();
    let high = *nums.iter().max().unwrap();
    nums.iter().filter(|&&x| low < x && x < high).count() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2148;
    let mut pool: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) * 7 % 200001 - 100000).collect();
    let mut total = 0;
    let mut check = 0;
    for round in 0..200000 {
        let at = (next_random(&mut seed) % 100000) as usize;
        pool[at] = next_random(&mut seed) % 21 - 10;
        let from = (next_random(&mut seed) % (100000 - 100)) as usize;
        let nums = pool[from..from + 100].to_vec();
        let count = count_elements(&nums);
        total += count;
        check = (check * 31 + count + round) % 1000000007;
    }
    println!("200000 counts: {} counted in all, checksum {}", total, check);
}
