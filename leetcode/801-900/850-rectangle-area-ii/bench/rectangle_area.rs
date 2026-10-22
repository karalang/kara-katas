// Benchmark for #850: Rectangle Area II -- Rust twin of the Kāra
// segment-tree arm (a sweep line over a segment tree).

struct Cover {
    ys: Vec<i64>,
    count: Vec<i64>,
    length: Vec<i64>,
}

fn update(t: &mut Cover, node: usize, lo: usize, hi: usize, a: usize, b: usize, delta: i64) {
    if b <= lo || hi <= a {
        return;
    }
    if a <= lo && hi <= b {
        t.count[node] += delta;
    } else {
        let mid = (lo + hi) / 2;
        update(t, 2 * node, lo, mid, a, b, delta);
        update(t, 2 * node + 1, mid, hi, a, b, delta);
    }
    if t.count[node] > 0 {
        t.length[node] = t.ys[hi] - t.ys[lo];
    } else if hi - lo == 1 {
        t.length[node] = 0;
    } else {
        t.length[node] = t.length[2 * node] + t.length[2 * node + 1];
    }
}

fn rectangle_area(rectangles: &[[i64; 4]]) -> i64 {
    let mut ys: Vec<i64> = Vec::new();
    let mut events: Vec<(i64, i64, i64, i64)> = Vec::new();
    for r in rectangles.iter() {
        ys.push(r[1]);
        ys.push(r[3]);
        events.push((r[0], 1, r[1], r[3]));
        events.push((r[2], -1, r[1], r[3]));
    }
    ys.sort();
    ys.dedup();
    events.sort();
    let segments = ys.len() - 1;
    let mut t = Cover { ys: ys.clone(), count: vec![0; 4 * ys.len()], length: vec![0; 4 * ys.len()] };
    let mut area = 0;
    let mut prev_x = 0;
    for &(x, delta, y1, y2) in events.iter() {
        area += t.length[1] * (x - prev_x);
        prev_x = x;
        if segments > 0 {
            let a = ys.binary_search(&y1).unwrap();
            let b = ys.binary_search(&y2).unwrap();
            update(&mut t, 1, 0, segments, a, b, delta);
        }
    }
    area % 1000000007
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 8000;
    let n = 200;
    let limit: i64 = 1000000000;
    let mut seed: i64 = 850;
    let mut sets: Vec<Vec<[i64; 4]>> = Vec::new();
    for g in 0..count {
        let size = limit >> (g % 8);
        let mut rectangles: Vec<[i64; 4]> = Vec::new();
        for _ in 0..n {
            let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (size + 1);
            let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (size + 1);
            let c = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (size + 1);
            let d = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (size + 1);
            rectangles.push([a.min(b), c.min(d), a.max(b), c.max(d)]);
        }
        sets.push(rectangles);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let a = rectangle_area(&sets[round % count]);
        total += a;
        checksum = (checksum * 31 + a) % 1000000007;
    }
    println!("{} rounds of {} sets: areas sum to {}, checksum {}", rounds, count, total, checksum);
}
