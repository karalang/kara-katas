// LeetCode #2090: K Radius Subarray Averages -- Rust mirror of the ★ arm's
// benchmark (averages.kara): the same 30 arrays, each asked for the same 10
// radii, one slide of the window into a fresh `Vec` each.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn get_averages(nums: &[i64], k: usize) -> Vec<i64> {
    let n = nums.len();
    let width = 2 * k + 1;
    let mut avgs = vec![-1i64; n];
    let mut sum = 0i64;
    for i in 0..n {
        sum += nums[i];
        if i >= width {
            sum -= nums[i - width];
        }
        if i + 1 >= width {
            avgs[i - k] = sum / width as i64;
        }
    }
    avgs
}

fn main() {
    let mut seed = 2090i64;
    let arrays: Vec<Vec<i64>> = (0..30)
        .map(|_| (0..100000).map(|_| next_random(&mut seed) % 100001).collect())
        .collect();
    let radii = [0, 1, 3, 10, 30, 100, 300, 1000, 3000, 20000];
    let (mut total, mut check) = (0i64, 0i64);
    for nums in &arrays {
        for &k in &radii {
            let s: i64 = get_averages(nums, k).iter().sum();
            total += s;
            check = (check * 31 + s) % 1000000007;
        }
    }
    println!("300 answers: sum {}, checksum {}", total, check);
}
