// LeetCode #2860: Happy Students -- the bench: the ★ arm over 50
// classes of 10^5 students, LeetCode's most, half of them random and
// half built around a group size, all drawn first, then each answered 20
// times, the sort included.

fn count_ways(nums: &[i64]) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let n = sorted.len();
    let mut ways = 0;
    for k in 0..=n {
        let chosen_ok = k == 0 || sorted[k - 1] < k as i64;
        let left_ok = k == n || sorted[k] > k as i64;
        if chosen_ok && left_ok {
            ways += 1;
        }
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn class(n: i64, seed: &mut i64) -> Vec<i64> {
    if next_random(seed) % 2 == 0 {
        return (0..n).map(|_| wide(seed) % n).collect();
    }
    let g = wide(seed) % (n + 1);
    let mut nums: Vec<i64> = (0..n).map(|i| if i < g { wide(seed) % g.max(1) } else { g + 1 + wide(seed) % (n - g).max(1) }).collect();
    for x in nums.iter_mut() {
        *x = (*x).min(n - 1);
    }
    if next_random(seed) % 4 == 0 {
        let at = (wide(seed) % n) as usize;
        nums[at] = g.min(n - 1);
    }
    for i in (1..n as usize).rev() {
        let j = (wide(seed) % (i as i64 + 1)) as usize;
        nums.swap(i, j);
    }
    nums
}

fn main() {
    let count = 50;
    let rounds = 20;
    let n = 100000;
    let mut seed = 2860;
    let classes: Vec<Vec<i64>> = (0..count).map(|_| class(n, &mut seed)).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in classes.iter() {
            let ways = count_ways(nums);
            total += ways;
            check = (check * 31 + ways + r) % 1000000007;
        }
    }
    println!("{count} classes of {n}, {rounds} rounds: {total} ways, checksum {check}");
}
