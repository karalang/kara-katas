// LeetCode #2027: Minimum Moves to Convert String -- the ★ arm in Rust, the
// same algorithm and workload as moves.kara: the string's chars collected,
// then a move at the leftmost X and a jump of three.

fn minimum_moves(s: &str) -> i64 {
    let key: Vec<char> = s.chars().collect();
    let mut moves = 0;
    let mut i = 0;
    while i < key.len() {
        if key[i] == 'X' {
            moves += 1;
            i += 3;
        } else {
            i += 1;
        }
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2027;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..2000 {
        let share = next_random(&mut seed) % 101;
        let mut s = String::new();
        for _ in 0..1000 {
            s.push(if next_random(&mut seed) % 100 < share { 'X' } else { 'O' });
        }
        strings.push(s);
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..50 {
        for s in &strings {
            let moves = minimum_moves(s);
            calls += 1;
            total += moves;
            check = (check * 31 + moves) % 1000000007;
        }
    }
    println!("{} calls: {} moves, checksum {}", calls, total, check);
}
