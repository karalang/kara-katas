// LeetCode #2293: Min Max Game -- the bench, the ★ arm in Rust. The
// rounds played in place on a copy of the array.

fn min_max_game(nums: &[i64]) -> i64 {
    let mut a = nums.to_vec();
    let mut n = a.len();
    while n > 1 {
        n /= 2;
        for i in 0..n {
            a[i] = if i % 2 == 0 { a[2 * i].min(a[2 * i + 1]) } else { a[2 * i].max(a[2 * i + 1]) };
        }
    }
    a[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2293;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..200 {
        let mut nums = Vec::new();
        for _ in 0..1024 {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        let mut total = 0;
        for nums in &arrays {
            total += min_max_game(nums);
        }
        check = (check * 31 + total) % 1000000007;
    }
    println!("50 passes over 200 arrays of 1024: checksum {}", check);
}
