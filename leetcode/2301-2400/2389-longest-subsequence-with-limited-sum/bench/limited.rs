// LeetCode #2389: Longest Subsequence With Limited Sum -- the bench, the
// ★ arm in Rust: the values sorted into prefix sums, each query answered
// by binary search.

fn answer_queries(nums: &[i64], queries: &[i64]) -> Vec<i64> {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut prefix: Vec<i64> = Vec::new();
    let mut running = 0i64;
    for &v in &sorted {
        running += v;
        prefix.push(running);
    }
    let mut answer: Vec<i64> = Vec::new();
    for &q in queries {
        let mut low = 0usize;
        let mut high = prefix.len();
        while low < high {
            let mid = (low + high) / 2;
            if prefix[mid] <= q {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        answer.push(low as i64);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    // 100 arrays of 1000 values up to 10^6, each with 1000 queries up to
    // 10^9; each pass answers them all and folds every answer
    let mut seed = 2389i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut asks: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        arrays.push((0..1000).map(|_| 1 + wide(&mut seed) % 1000000).collect());
        asks.push((0..1000).map(|_| 1 + wide(&mut seed) % 1000000000).collect());
    }
    let mut check = 0i64;
    for p in 0..200i64 {
        for a in 0..100usize {
            for v in answer_queries(&arrays[a], &asks[a]) {
                check = (check * 31 + v + p) % 1000000007;
            }
        }
    }
    println!("200 passes over 100 arrays of 1000 values and 1000 queries: checksum {}", check);
}
