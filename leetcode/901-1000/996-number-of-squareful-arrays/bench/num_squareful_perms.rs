// Benchmark: LeetCode #996 Number of Squareful Arrays -- the ★ arm,
// backtracking over the sorted values, on random arrays of 12 values,
// LeetCode's largest. Mirrors num_squareful_perms.kara, .c, .py and
// go-seq/.

fn is_square(s: i64) -> bool {
    let mut r = (s as f64).sqrt() as i64;
    while r * r > s {
        r -= 1;
    }
    while (r + 1) * (r + 1) <= s {
        r += 1;
    }
    r * r == s
}

fn place(a: &[i64], used: &mut [bool], depth: usize, last: i64) -> i64 {
    let n = a.len();
    if depth == n {
        return 1;
    }
    let mut count = 0;
    for i in 0..n {
        if used[i] {
            continue;
        }
        if i > 0 && a[i] == a[i - 1] && !used[i - 1] {
            continue;
        }
        if depth > 0 && !is_square(last + a[i]) {
            continue;
        }
        used[i] = true;
        count += place(a, used, depth + 1, a[i]);
        used[i] = false;
    }
    count
}

fn num_squareful_perms(nums: &[i64]) -> i64 {
    let mut a = nums.to_vec();
    a.sort();
    let mut used = vec![false; a.len()];
    place(&a, &mut used, 0, 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// 12 values below 50, each making a square with the one before
fn random_walk(seed: &mut i64) -> Vec<i64> {
    let mut nums = vec![next_random(seed) % 50];
    for _ in 1..12 {
        let v = nums[nums.len() - 1];
        let mut options = Vec::new();
        let mut r = 0;
        while r * r < v + 50 {
            if r * r >= v {
                options.push(r * r - v);
            }
            r += 1;
        }
        nums.push(options[(next_random(seed) % options.len() as i64) as usize]);
    }
    nums
}

fn main() {
    let rounds = 300;
    let mut seed = 996;
    let arrays: Vec<Vec<i64>> = (0..20).map(|_| random_walk(&mut seed)).collect();
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let got = num_squareful_perms(&arrays[(r + i) % 20]);
            found += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 arrays of 12 values: {found} squareful permutations, checksum {check}");
}
