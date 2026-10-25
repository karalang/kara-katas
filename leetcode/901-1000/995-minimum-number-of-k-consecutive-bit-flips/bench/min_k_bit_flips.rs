// Benchmark: LeetCode #995 Minimum Number of K Consecutive Bit Flips --
// the ★ arm, the greedy with a running parity, on random arrays of
// 100000 bits, LeetCode's largest. Mirrors min_k_bit_flips.kara, .c, .py
// and go-seq/.

fn min_k_bit_flips(nums: &[i64], k: usize) -> i64 {
    let n = nums.len();
    let mut ends = vec![false; n + 1];
    let mut flipped = false;
    let mut flips = 0;
    for i in 0..n {
        if ends[i] {
            flipped = !flipped;
        }
        if (nums[i] == 1) == flipped {
            if i + k > n {
                return -1;
            }
            flips += 1;
            flipped = !flipped;
            ends[i + k] = true;
        }
    }
    flips
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 50;
    let mut seed = 995;
    // ten arrays of random bits and ten of ones put through random flips
    // of 1 to 100 bits, which can be made all ones again
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<usize> = Vec::new();
    for a in 0..20 {
        if a % 2 == 0 {
            let nums: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 2).collect();
            arrays.push(nums);
            ks.push(1 + (next_random(&mut seed) % 100) as usize);
        } else {
            let k = 1 + (next_random(&mut seed) % 100) as usize;
            let mut nums = vec![1i64; 100000];
            for i in 0..100000 - k + 1 {
                if next_random(&mut seed) % 4 == 0 {
                    for j in i..i + k {
                        nums[j] = 1 - nums[j];
                    }
                }
            }
            arrays.push(nums);
            ks.push(k);
        }
    }
    let mut stuck: i64 = 0;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let a = (r + i) % 20;
            let got = min_k_bit_flips(&arrays[a], ks[a]);
            if got < 0 {
                stuck += 1;
            } else {
                total += got;
            }
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 arrays of 100000 bits: {stuck} impossible, {total} flips, checksum {check}");
}
