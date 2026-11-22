// LeetCode #2741: Special Permutations -- the bench (special.kara in
// Rust): ways[mask][last] carried forward to every partner of `last`.

const MOD: i64 = 1000000007;

fn special_perm(nums: &[i64]) -> i64 {
    let n = nums.len();
    let full = (1usize << n) - 1;
    let mut ways: Vec<Vec<i64>> = vec![vec![0; n]; 1 << n];
    for i in 0..n {
        ways[1 << i][i] = 1;
    }
    for mask in 1..full {
        for last in 0..n {
            let w = ways[mask][last];
            if w == 0 {
                continue;
            }
            for next in 0..n {
                if (mask >> next) & 1 == 0 && (nums[next] % nums[last] == 0 || nums[last] % nums[next] == 0) {
                    let to = mask | (1 << next);
                    ways[to][next] = (ways[to][next] + w) % MOD;
                }
            }
        }
    }
    let mut total = 0;
    for last in 0..n {
        total = (total + ways[full][last]) % MOD;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 30;
    let rounds: i64 = 5;
    let mut seed = 2741;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < 14 {
            let a = next_random(&mut seed) % 6;
            let b = next_random(&mut seed) % 4;
            let x = (1i64 << a) * [1, 3, 9, 27][b as usize];
            if !nums.contains(&x) {
                nums.push(x);
            }
        }
        arrays.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let k = special_perm(nums);
            sum += k;
            check = (check * 31 + k + r) % 1000000007;
        }
    }
    println!("{} arrays of 14 numbers, {} rounds: counts sum to {}, checksum {}", count, rounds, sum, check);
}
