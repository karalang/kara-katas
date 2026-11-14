// LeetCode #1564: Put Boxes Into the Warehouse I -- bench: the ★ arm
// (usable heights, the smallest boxes into the deepest rooms) over 20
// problems of 100000 boxes and 100000 rooms, built once, each asked 10
// times.
// Rust mirror of warehouse.kara.

fn max_boxes_in_warehouse(boxes: &[i64], warehouse: &[i64]) -> i64 {
    let mut usable = warehouse.to_vec();
    for i in 1..usable.len() {
        usable[i] = usable[i].min(usable[i - 1]);
    }
    let mut sorted = boxes.to_vec();
    sorted.sort();
    let mut placed = 0;
    for &room in usable.iter().rev() {
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
    let top = 1000000000i64;
    let mut seed = 1564;
    let mut problems: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..20 {
        let mut boxes = Vec::new();
        for _ in 0..100000 {
            boxes.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % top + 1);
        }
        let mut warehouse = Vec::new();
        for _ in 0..100000 {
            warehouse.push(top - (next_random(&mut seed) * 32768 + next_random(&mut seed)) % ((top + 1) / 2));
        }
        problems.push((boxes, warehouse));
    }
    let mut check = 0;
    let mut total = 0;
    for _ in 0..10 {
        for (boxes, warehouse) in &problems {
            let placed = max_boxes_in_warehouse(boxes, warehouse);
            total += placed;
            check = mix(check, placed);
        }
    }
    println!("10 passes over 20 problems of 100000 boxes and rooms: {} boxes, checksum {}", total, check);
}
