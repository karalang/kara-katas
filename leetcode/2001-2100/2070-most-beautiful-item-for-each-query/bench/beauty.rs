// LeetCode #2070: Most Beautiful Item for Each Query -- Rust mirror of the
// ★ arm's benchmark (beauty.kara): 20 shops of 100000 items and 100000
// queries each, prices, beauties and queries up to 10^9.

fn maximum_beauty(items: &[Vec<i64>], queries: &[i64]) -> Vec<i64> {
    let mut sorted = items.to_vec();
    sorted.sort_by_key(|item| item[0]);
    let mut best = Vec::new();
    let mut most = 0;
    for item in &sorted {
        most = most.max(item[1]);
        best.push(most);
    }
    queries
        .iter()
        .map(|&q| {
            let end = sorted.partition_point(|item| item[0] <= q);
            if end == 0 { 0 } else { best[end - 1] }
        })
        .collect()
}

fn main() {
    let mut seed: i64 = 2070;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut up_to = |top: i64| {
        let hi = next_random();
        (hi * 32768 + next_random()) % top + 1
    };
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..20 {
        let mut items = Vec::new();
        for _ in 0..100000 {
            let p = up_to(1000000000);
            items.push(vec![p, up_to(1000000000)]);
        }
        let queries: Vec<i64> = (0..100000).map(|_| up_to(1000000000)).collect();
        for a in maximum_beauty(&items, &queries) {
            sum += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("20 shops: sum {sum}, checksum {check}");
}
