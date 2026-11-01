// LeetCode #1036: Escape a Large Maze -- bench
// Mirrors ./escape_maze.kara; see ../README.md § Benchmarks. Both sets are
// std's HashSet, SipHash-1-3 like Kāra's Set.

use std::collections::{HashSet, VecDeque};

fn not_fenced(blocked: &HashSet<(i64, i64)>, from: (i64, i64), to: (i64, i64), side: i64) -> bool {
    let limit = blocked.len() * (blocked.len().max(1) - 1) / 2;
    let mut seen: HashSet<(i64, i64)> = HashSet::new();
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    seen.insert(from);
    queue.push_back(from);
    while let Some((x, y)) = queue.pop_front() {
        if (x, y) == to || seen.len() > limit {
            return true;
        }
        for (dx, dy) in vec![(1i64, 0i64), (-1, 0), (0, 1), (0, -1)].iter() {
            let next = (x + dx, y + dy);
            let (nx, ny) = next;
            if nx >= 0 && nx < side && ny >= 0 && ny < side && !blocked.contains(&next) && !seen.contains(&next) {
                seen.insert(next);
                queue.push_back(next);
            }
        }
    }
    false
}

fn escape_within(blocked: &[(i64, i64)], source: (i64, i64), target: (i64, i64), side: i64) -> bool {
    let walls: HashSet<(i64, i64)> = blocked.iter().cloned().collect();
    not_fenced(&walls, source, target, side) && not_fenced(&walls, target, source, side)
}

fn is_escape_possible(blocked: &[(i64, i64)], source: (i64, i64), target: (i64, i64)) -> bool {
    escape_within(blocked, source, target, 1000000)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 4;
    let mut seed = 1036;
    let mut mazes: Vec<(Vec<(i64, i64)>, (i64, i64), (i64, i64))> = Vec::new();
    for k in 0..30 {
        let mut blocked: Vec<(i64, i64)> = Vec::new();
        let cx = next_random(&mut seed) % 900000 + 50000;
        let cy = next_random(&mut seed) % 900000 + 50000;
        if k % 3 == 2 {
            for i in 0..200 {
                blocked.push((i, 199 - i));
            }
            mazes.push((blocked, (200, 0), (cx, cy)));
        } else {
            for i in 0..50 {
                blocked.push((cx + i, cy + 50 - i));
                blocked.push((cx + 50 - i, cy - i));
                blocked.push((cx - i, cy - 50 + i));
                blocked.push((cx - 50 + i, cy + i));
            }
            let inside = (cx + 10, cy - 10);
            let outside = (cx + 60, cy);
            if k % 3 == 0 {
                mazes.push((blocked, inside, (0, 0)));
            } else {
                mazes.push((blocked, outside, (999999, 999999)));
            }
        }
    }
    let mut escapes = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for (blocked, source, target) in mazes.iter() {
            let answer = is_escape_possible(blocked, *source, *target);
            if answer {
                escapes += 1;
            }
            check = (check * 131 + if answer { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("30 mazes of 200 blocks, {} rounds: {} escapes, checksum {}", rounds, escapes, check);
}
