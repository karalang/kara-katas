// LeetCode #2089: Find Target Indices After Sorting Array -- Rust mirror of
// the ★ arm's benchmark (target.kara): the same 10000 arrays, each asked for
// every target, two counts and the indices collected into a fresh `Vec`.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn target_indices(nums: &[i64], target: i64) -> Vec<i64> {
    let less = nums.iter().filter(|&&x| x < target).count() as i64;
    let equal = nums.iter().filter(|&&x| x == target).count() as i64;
    (less..less + equal).collect()
}

fn main() {
    let mut seed = 2089i64;
    let arrays: Vec<Vec<i64>> = (0..10000)
        .map(|_| (0..100).map(|_| next_random(&mut seed) % 100 + 1).collect())
        .collect();
    let (mut total, mut check) = (0i64, 0i64);
    for nums in &arrays {
        for target in 1..=100 {
            let got = target_indices(nums, target);
            for &i in &got {
                total += i * target;
            }
            check = (check * 31 + got.len() as i64 * 100 + got.first().copied().unwrap_or(0)) % 1000000007;
        }
    }
    println!("1000000 answers: sum {}, checksum {}", total, check);
}
