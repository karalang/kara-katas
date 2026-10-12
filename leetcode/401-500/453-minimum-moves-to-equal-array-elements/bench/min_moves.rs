// Benchmark for #453: mirror of min_moves.kara (the ★ arm, sum minus n
// times the minimum) on the same workload.

fn min_moves(nums: &[i64]) -> i64 {
    let mut smallest = nums[0];
    let mut total = 0;
    for &x in nums {
        smallest = smallest.min(x);
        total += x;
    }
    total - nums.len() as i64 * smallest
}

// ---- benchmark --------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 65536 + lo) % 2000000001 - 1000000000
}

fn main() {
    let arrays = 10;
    let n: i64 = 1000000;
    let rounds = 20;
    let mut seed: i64 = 453;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            nums.push(random_value(&mut seed));
        }
        all.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for a in 0..arrays {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let at = ((hi * 65536 + lo) % n) as usize;
            all[a][at] = random_value(&mut seed);
            let moves = min_moves(&all[a]);
            total += moves;
            checksum = (checksum * 31 + moves % 1000000007) % 1000000007;
        }
    }
    println!("{rounds} rounds on {arrays} arrays of {n}: {total} moves, checksum {checksum}");
}
