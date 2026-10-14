// Benchmark for #554: Rust mirror of the ★ arm (count the edges at each
// position); see brick_wall.kara.
use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn least_bricks(wall: &[Vec<i64>]) -> i64 {
    let mut edges: HashMap<i64, i64> = HashMap::new();
    let mut most = 0;
    for row in wall {
        let mut at = 0;
        for j in 0..row.len() - 1 {
            at += row[j];
            let count = edges.get(&at).copied().unwrap_or(0) + 1;
            edges.insert(at, count);
            if count > most {
                most = count;
            }
        }
    }
    wall.len() as i64 - most
}

fn main() {
    let count = 20;
    let mut seed: i64 = 554;
    let mut walls: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut bricks = 0;
    for _ in 0..count {
        let mut wall: Vec<Vec<i64>> = Vec::new();
        let mut n = 0;
        while n < 19000 {
            let mut row: Vec<i64> = Vec::new();
            let mut left = 1000000;
            while left > 0 {
                let a = next_random(&mut seed);
                let b = next_random(&mut seed);
                let w = (1 + (a * 32768 + b) % 10000).min(left);
                row.push(w);
                left -= w;
            }
            n += row.len();
            wall.push(row);
        }
        bricks += n;
        walls.push(wall);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..50 {
        for g in 0..count {
            let got = least_bricks(&walls[(round * 7 + g) % count]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} walls, {} bricks, 50 rounds each: total {}, checksum {}", count, bricks, total, checksum);
}
