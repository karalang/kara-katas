// LeetCode #2176: Count Equal and Divisible Pairs in an Array -- the
// benchmark's Rust mirror of pairs.kara.

fn count_pairs(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let mut pairs = 0i64;
    for i in 0..n {
        for j in (i + 1)..n {
            if nums[i] == nums[j] && (i * j) as i64 % k == 0 {
                pairs += 1;
            }
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2176i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        row.push(next_random(&mut seed) % 5 + 1);
    }
    let mut check = 0i64;
    for _ in 0..20000 {
        let start = (next_random(&mut seed) % 99901) as usize;
        let k = next_random(&mut seed) % 100 + 1;
        let pairs = count_pairs(&row[start..start + 100], k);
        check = (check * 31 + pairs) % 1000000007;
    }
    println!("20000 solves: checksum {}", check);
}
