// LeetCode #1728: Cat and Mouse II -- the bench (mouse.kara): the game
// solved backwards from its ends, a state lost for the player to move
// once every move from it is counted off.

use std::collections::VecDeque;

fn reach(marks: &[Vec<u8>], at: usize, jump: i32) -> Vec<usize> {
    let rows = marks.len() as i64;
    let cols = marks[0].len() as i64;
    let (r, c) = (at as i64 / cols, at as i64 % cols);
    let mut cells = vec![at];
    for (dr, dc) in [(0i64, 1i64), (1, 0), (0, -1), (-1, 0)] {
        for k in 1..jump as i64 + 1 {
            let (nr, nc) = (r + dr * k, c + dc * k);
            if nr < 0
                || nr >= rows
                || nc < 0
                || nc >= cols
                || marks[nr as usize][nc as usize] == b'#'
            {
                break;
            }
            cells.push((nr * cols + nc) as usize);
        }
    }
    cells
}

fn can_mouse_win(grid: &[String], cat_jump: i32, mouse_jump: i32) -> bool {
    let marks: Vec<Vec<u8>> = grid.iter().map(|row| row.as_bytes().to_vec()).collect();
    let cols = marks[0].len();
    let cells = marks.len() * cols;
    let (mut mouse, mut cat, mut food) = (0, 0, 0);
    for at in 0..cells {
        match marks[at / cols][at % cols] {
            b'M' => mouse = at,
            b'C' => cat = at,
            b'F' => food = at,
            _ => {}
        }
    }
    let open: Vec<bool> = (0..cells)
        .map(|at| marks[at / cols][at % cols] != b'#')
        .collect();
    let mouse_moves: Vec<Vec<usize>> = (0..cells)
        .map(|at| {
            if open[at] {
                reach(&marks, at, mouse_jump)
            } else {
                Vec::new()
            }
        })
        .collect();
    let cat_moves: Vec<Vec<usize>> = (0..cells)
        .map(|at| {
            if open[at] {
                reach(&marks, at, cat_jump)
            } else {
                Vec::new()
            }
        })
        .collect();
    let state = |m: usize, c: usize, turn: usize| (m * cells + c) * 2 + turn;
    let mut result = vec![0i32; cells * cells * 2];
    let mut left = vec![0usize; cells * cells * 2];
    let mut queue: VecDeque<usize> = VecDeque::new();
    for m in 0..cells {
        for c in 0..cells {
            if !open[m] || !open[c] {
                continue;
            }
            left[state(m, c, 0)] = mouse_moves[m].len();
            left[state(m, c, 1)] = cat_moves[c].len();
            let end = if m == c || c == food {
                2
            } else if m == food {
                1
            } else {
                0
            };
            if end != 0 {
                for turn in 0..2 {
                    result[state(m, c, turn)] = end;
                    queue.push_back(state(m, c, turn));
                }
            }
        }
    }
    while let Some(s) = queue.pop_front() {
        let turn = s % 2;
        let m = s / 2 / cells;
        let c = s / 2 % cells;
        let won = result[s];
        if turn == 0 {
            for &before in cat_moves[c].iter() {
                let p = state(m, before, 1);
                if result[p] != 0 {
                    continue;
                }
                if won == 2 {
                    result[p] = 2;
                    queue.push_back(p);
                } else {
                    left[p] -= 1;
                    if left[p] == 0 {
                        result[p] = 1;
                        queue.push_back(p);
                    }
                }
            }
        } else {
            for &before in mouse_moves[m].iter() {
                let p = state(before, c, 0);
                if result[p] != 0 {
                    continue;
                }
                if won == 1 {
                    result[p] = 1;
                    queue.push_back(p);
                } else {
                    left[p] -= 1;
                    if left[p] == 0 {
                        result[p] = 2;
                        queue.push_back(p);
                    }
                }
            }
        }
    }
    result[state(mouse, cat, 0)] == 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200;
    let rounds: i64 = 20;
    let side: i64 = 8;
    let cells = side * side;
    let mut seed: i64 = 1728;
    let mut problems: Vec<(Vec<String>, i32, i32)> = Vec::new();
    for _ in 0..count {
        let mut marks: Vec<u8> = (0..cells)
            .map(|_| {
                if next_random(&mut seed) % 4 == 0 {
                    b'#'
                } else {
                    b'.'
                }
            })
            .collect();
        let mut places: Vec<usize> = (0..cells as usize).collect();
        for i in 0..3 {
            let j = i + (next_random(&mut seed) % (cells - i as i64)) as usize;
            places.swap(i, j);
        }
        marks[places[0]] = b'C';
        marks[places[1]] = b'M';
        marks[places[2]] = b'F';
        let grid: Vec<String> = (0..side as usize)
            .map(|r| {
                String::from_utf8(marks[r * side as usize..(r + 1) * side as usize].to_vec())
                    .unwrap()
            })
            .collect();
        let cat_jump = (next_random(&mut seed) % side + 1) as i32;
        let mouse_jump = (next_random(&mut seed) % side + 1) as i32;
        problems.push((grid, cat_jump, mouse_jump));
    }
    let mut wins = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (grid, cat_jump, mouse_jump) in problems.iter() {
            let answer = can_mouse_win(grid, *cat_jump, *mouse_jump);
            if answer {
                wins += 1;
            }
            check = (check * 31 + if answer { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!(
        "{} grids of {} by {}, {} rounds: the mouse wins {}, checksum {}",
        count, side, side, rounds, wins, check
    );
}
