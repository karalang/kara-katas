// LeetCode #1197 bench: the ★ arm in Rust, over the same 2000 random
// targets as the Kāra bench.

use std::collections::VecDeque;

const MOVES: [(i64, i64); 8] = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)];

fn min_knight_moves(x: i64, y: i64) -> i64 {
    let tx = x.abs();
    let ty = y.abs();
    let side = 305;
    let mut seen = vec![false; (side * side) as usize];
    let mut queue = VecDeque::new();
    queue.push_back((0i64, 0i64, 0i64));
    seen[(2 * side + 2) as usize] = true;
    while let Some((cx, cy, steps)) = queue.pop_front() {
        if cx == tx && cy == ty {
            return steps;
        }
        for &(dx, dy) in MOVES.iter() {
            let nx = cx + dx;
            let ny = cy + dy;
            if nx >= -2 && ny >= -2 && nx <= 302 && ny <= 302 {
                let k = ((nx + 2) * side + ny + 2) as usize;
                if !seen[k] {
                    seen[k] = true;
                    queue.push_back((nx, ny, steps + 1));
                }
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1197;
    let mut targets = Vec::new();
    for _ in 0..2000 {
        let s = next_random(&mut seed) % 301;
        let x = next_random(&mut seed) % (s + 1);
        let y = s - x;
        let x = if next_random(&mut seed) % 2 == 0 { x } else { -x };
        let y = if next_random(&mut seed) % 2 == 0 { y } else { -y };
        targets.push((x, y));
    }
    let mut check: i64 = 0;
    for &(x, y) in &targets {
        let m = min_knight_moves(x, y);
        check = (check * 131 + m + 1) % 1000000007;
    }
    println!("2000 targets: checksum {}", check);
}
