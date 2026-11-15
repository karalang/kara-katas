// LeetCode #1580 bench: the same usable heights matched smallest first, in
// Rust.

fn max_boxes_in_warehouse(boxes: &[i64], warehouse: &[i64]) -> i64 {
    let m = warehouse.len();
    let mut from_left = warehouse.to_vec();
    for i in 1..m {
        from_left[i] = from_left[i].min(from_left[i - 1]);
    }
    let mut usable = warehouse.to_vec();
    for i in (0..m - 1).rev() {
        usable[i] = usable[i].min(usable[i + 1]);
    }
    for i in 0..m {
        usable[i] = usable[i].max(from_left[i]);
    }
    usable.sort();
    let mut sorted = boxes.to_vec();
    sorted.sort();
    let mut placed = 0usize;
    for &room in usable.iter() {
        if placed < sorted.len() && sorted[placed] <= room {
            placed += 1;
        }
    }
    placed as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1580i64;
    let mut problems: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..40 {
        let boxes: Vec<i64> = (0..100000)
            .map(|_| (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1)
            .collect();
        let warehouse: Vec<i64> = (0..100000i64)
            .map(|i| {
                let valley = (i - 50000).abs() * 20000;
                valley + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000
            })
            .collect();
        problems.push((boxes, warehouse));
    }
    let (mut check, mut total) = (0i64, 0i64);
    for (boxes, warehouse) in problems.iter() {
        let placed = max_boxes_in_warehouse(boxes, warehouse);
        total += placed;
        check = mix(check, placed);
    }
    println!("40 problems of 100000 boxes and rooms: boxes placed {}, checksum {}", total, check);
}
