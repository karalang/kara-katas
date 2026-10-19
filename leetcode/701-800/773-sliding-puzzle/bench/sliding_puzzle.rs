// LeetCode 773 — Sliding Puzzle: benchmark, the ★ arm in Rust.
// All 720 boards, in dictionary order, built once; ROUNDS rounds each
// solve the next of them. HashSet<String> hashes with SipHash-1-3.
use std::collections::{HashSet, VecDeque};

const ROUNDS: i64 = 20000;
const NEIGHBOURS: [&[usize]; 6] = [&[1, 3], &[0, 2, 4], &[1, 5], &[0, 4], &[1, 3, 5], &[2, 4]];

fn sliding_puzzle(board: &[Vec<i64>]) -> i64 {
    let mut start = String::new();
    for row in board {
        for &x in row {
            start.push((48 + x) as u8 as char);
        }
    }
    let mut seen: HashSet<String> = HashSet::new();
    seen.insert(start.clone());
    let mut queue: VecDeque<(String, i64)> = VecDeque::new();
    queue.push_back((start, 0));
    while let Some((state, steps)) = queue.pop_front() {
        if state == "123450" {
            return steps;
        }
        let bytes = state.as_bytes().to_vec();
        let zero = bytes.iter().position(|&b| b == b'0').unwrap();
        for &next in NEIGHBOURS[zero] {
            let mut moved = bytes.clone();
            moved.swap(zero, next);
            let text = String::from_utf8(moved).unwrap();
            if !seen.contains(&text) {
                seen.insert(text.clone());
                queue.push_back((text, steps + 1));
            }
        }
    }
    -1
}

fn next_order(cells: &mut [i64]) -> bool {
    let mut i = cells.len() as i64 - 2;
    while i >= 0 && cells[i as usize] >= cells[i as usize + 1] {
        i -= 1;
    }
    if i < 0 {
        return false;
    }
    let i = i as usize;
    let mut j = cells.len() - 1;
    while cells[j] <= cells[i] {
        j -= 1;
    }
    cells.swap(i, j);
    cells[i + 1..].reverse();
    true
}

fn main() {
    let mut boards: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut cells = vec![0i64, 1, 2, 3, 4, 5];
    loop {
        boards.push(vec![cells[0..3].to_vec(), cells[3..6].to_vec()]);
        if !next_order(&mut cells) {
            break;
        }
    }
    let mut solved = 0;
    let mut check: i64 = 0;
    for round in 0..ROUNDS {
        let answer = sliding_puzzle(&boards[(round % 720) as usize]);
        if answer >= 0 {
            solved += 1;
        }
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("{ROUNDS} boards: {solved} solvable, checksum {check}");
}
