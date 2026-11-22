// LeetCode #2717: Semi-Ordered Permutation -- the bench (semi.kara in
// Rust): 1's index plus n's distance from the end, less one when 1 starts
// right of n, the indices found by `position`.

fn semi_ordered_permutation(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let first = nums.iter().position(|&v| v == 1).unwrap() as i64;
    let last = nums.iter().position(|&v| v == n).unwrap() as i64;
    let swaps = first + (n - 1 - last);
    if first > last { swaps - 1 } else { swaps }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200000;
    let rounds = 20;
    let mut seed: i64 = 2717;
    let mut perms: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = (1..=50).collect();
        for i in (1..50i64).rev() {
            let j = next_random(&mut seed) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        perms.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in perms.iter() {
            let swaps = semi_ordered_permutation(nums);
            sum += swaps;
            check = (check * 31 + swaps + r) % 1000000007;
        }
    }
    println!("{} permutations of 50, {} rounds: swaps sum to {}, checksum {}", count, rounds, sum, check);
}
