// LeetCode #2343: Query Kth Smallest Trimmed Number -- the bench, the ★ arm
// in Rust: for each query the indices sorted by their trimmed text, as an
// owned key, and then by index, and the k-th taken.

fn smallest_trimmed_numbers(nums: &[String], queries: &[Vec<i64>]) -> Vec<i64> {
    let width = nums[0].len();
    let mut answer = Vec::new();
    for query in queries {
        let (k, trim) = (query[0] as usize, query[1] as usize);
        let mut order: Vec<usize> = (0..nums.len()).collect();
        order.sort_by_key(|&i| (nums[i][width - trim..].to_string(), i));
        answer.push(order[k - 1] as i64);
    }
    answer
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let mut cases: Vec<(Vec<String>, Vec<Vec<i64>>)> = Vec::new();
    for c in 0..10i64 {
        let nums: Vec<String> = (0..100i64)
            .map(|i| (0..100i64).map(|d| char::from(b'0' + (scrambled(c * 10000 + i * 100 + d) % 10) as u8)).collect())
            .collect();
        let queries: Vec<Vec<i64>> = (0..100i64)
            .map(|q| vec![1 + scrambled(c * 1000 + q + 500000) % 100, 1 + scrambled(c * 1000 + q + 700000) % 100])
            .collect();
        cases.push((nums, queries));
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for (nums, queries) in &cases {
            for i in smallest_trimmed_numbers(nums, queries) {
                check = (check * 31 + i + p) % 1000000007;
            }
        }
    }
    println!("50 passes over 10 cases of 100 numbers of 100 digits under 100 queries: checksum {}", check);
}
