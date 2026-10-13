// Benchmark for #517: Rust mirror of the ★ arm (the flow across each
// gap); see find_min_moves.kara.

fn find_min_moves(machines: &[i64]) -> i64 {
    let n = machines.len() as i64;
    let mut total = 0;
    for m in machines.iter() {
        total += *m;
    }
    if total % n != 0 {
        return -1;
    }
    let average = total / n;
    let mut moves = 0;
    let mut surplus: i64 = 0;
    for m in machines.iter() {
        let extra = *m - average;
        surplus += extra;
        moves = moves.max(surplus.abs()).max(extra);
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 100 random rows of 10,000 machines (the problem's most) holding up
    // to 100,000 dresses each, every other row topped up so the dresses
    // share out evenly, built once. Then each is solved 300 times.
    let mut seed: i64 = 517;
    let rows = 100;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for t in 0..rows {
        let mut machines: Vec<i64> = Vec::new();
        let mut total = 0;
        for _ in 0..10000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let m = (a * 32768 + b) % 100001;
            machines.push(m);
            total += m;
        }
        if t % 2 == 0 {
            machines[9999] += (10000 - total % 10000) % 10000;
        }
        all.push(machines);
    }
    let mut checksum: i64 = 0;
    for _ in 0..300 {
        for t in 0..rows {
            checksum = (checksum * 31 + find_min_moves(&all[t]) + 1) % 1000000007;
        }
    }
    println!("{} rows of 10000 machines, 300 times each: checksum {}", rows, checksum);
}
