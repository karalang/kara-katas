// LeetCode #2772: Apply Operations to Make All Array Elements Equal to
// Zero -- the bench in Rust: the ★ arm over 20 arrays of 10^5 numbers,
// all drawn first, then each answered 40 times.

fn check_array(nums: &[i64], k: i64) -> bool {
    let n = nums.len() as i64;
    let mut ends = vec![0i64; (n + 1) as usize];
    let mut covering: i64 = 0;
    for i in 0..n {
        covering -= ends[i as usize];
        let left = nums[i as usize] - covering;
        if left < 0 {
            return false;
        }
        if left > 0 {
            if i + k > n {
                return false;
            }
            covering += left;
            ends[(i + k) as usize] += left;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn built(n: i64, k: i64, most: i64, seed: &mut i64) -> Vec<i64> {
    let mut nums = vec![0i64; n as usize];
    let mut ops = vec![0i64; n as usize];
    let mut running = 0;
    for i in 0..n {
        if i + k <= n {
            ops[i as usize] = next_random(seed) % (most + 1);
        }
        running += ops[i as usize];
        if i >= k {
            running -= ops[(i - k) as usize];
        }
        nums[i as usize] = running;
    }
    if next_random(seed) % 2 == 1 {
        let at = (wide(seed) % n) as usize;
        if nums[at] > 0 && next_random(seed) % 2 == 1 {
            nums[at] -= 1;
        } else {
            nums[at] += 1;
        }
    }
    nums
}

fn main() {
    let count = 20;
    let rounds = 40;
    let mut seed: i64 = 2772;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let k = wide(&mut seed) % 1000 + 1;
        cases.push((built(100000, k, 9, &mut seed), k));
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in cases.iter() {
            let a = check_array(nums, *k);
            if a {
                yes += 1;
            }
            check = (check * 31 + if a { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{} arrays of 10^5, {} rounds: {} true, checksum {}", count, rounds, yes, check);
}
