// Benchmark for #488: Rust mirror of the ★ arm (breadth first); see
// zuma_game.kara.
use std::collections::HashSet;

fn shrink(board: Vec<u8>) -> Vec<u8> {
    let mut b = board;
    loop {
        let mut kept: Vec<u8> = Vec::new();
        let mut removed = false;
        let mut i = 0;
        while i < b.len() {
            let mut j = i;
            while j < b.len() && b[j] == b[i] {
                j += 1;
            }
            if j - i >= 3 {
                removed = true;
            } else {
                kept.extend_from_slice(&b[i..j]);
            }
            i = j;
        }
        b = kept;
        if !removed {
            return b;
        }
    }
}

fn find_min_step(board: &str, hand: &str) -> i64 {
    let mut first: Vec<u8> = hand.bytes().collect();
    first.sort();
    let mut boards: Vec<Vec<u8>> = vec![board.bytes().collect()];
    let mut hands: Vec<Vec<u8>> = vec![first];
    let mut seen: HashSet<String> = HashSet::new();
    let mut steps = 0;
    while !boards.is_empty() {
        steps += 1;
        let mut next_boards: Vec<Vec<u8>> = Vec::new();
        let mut next_hands: Vec<Vec<u8>> = Vec::new();
        for s in 0..boards.len() {
            let b = &boards[s];
            let h = &hands[s];
            for t in 0..h.len() {
                let c = h[t];
                if t > 0 && h[t - 1] == c {
                    continue;
                }
                for i in 0..b.len() + 1 {
                    let starts_run = i < b.len() && b[i] == c && (i == 0 || b[i - 1] != c);
                    let splits_pair = i > 0 && i < b.len() && b[i - 1] == b[i] && b[i] != c;
                    if !starts_run && !splits_pair {
                        continue;
                    }
                    let mut inserted: Vec<u8> = Vec::with_capacity(b.len() + 1);
                    inserted.extend_from_slice(&b[..i]);
                    inserted.push(c);
                    inserted.extend_from_slice(&b[i..]);
                    let after = shrink(inserted);
                    if after.is_empty() {
                        return steps;
                    }
                    let mut rest = h.clone();
                    rest.remove(t);
                    let mut state = String::with_capacity(after.len() + rest.len() + 1);
                    state.push_str(std::str::from_utf8(&after).unwrap());
                    state.push('|');
                    state.push_str(std::str::from_utf8(&rest).unwrap());
                    if seen.insert(state) {
                        next_boards.push(after);
                        next_hands.push(rest);
                    }
                }
            }
        }
        boards = next_boards;
        hands = next_hands;
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let colours = [b'R', b'Y', b'B', b'G', b'W'];
    let mut boards: Vec<String> = Vec::new();
    let mut hands: Vec<String> = Vec::new();
    let mut seed: i64 = 488;
    for c in 0..60 {
        let palette = 2 + c % 3;
        let mut balls: Vec<u8> = Vec::new();
        while balls.len() < 16 {
            let ball = colours[(next_random(&mut seed) % palette) as usize];
            let n = balls.len();
            if n >= 2 && balls[n - 1] == ball && balls[n - 2] == ball {
                continue;
            }
            balls.push(ball);
        }
        boards.push(String::from_utf8(balls).unwrap());
        let mut hand: Vec<u8> = Vec::new();
        for _ in 0..5 {
            hand.push(colours[(next_random(&mut seed) % palette) as usize]);
        }
        hands.push(String::from_utf8(hand).unwrap());
    }
    let mut cleared = 0;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for k in 0..boards.len() {
        let steps = find_min_step(&boards[k], &hands[k]);
        if steps >= 0 {
            cleared += 1;
            total += steps;
        }
        checksum = (checksum * 31 + steps + 2) % 1000000007;
    }
    println!("60 cases of 16 balls and a hand of 5: {cleared} cleared with {total} balls, checksum {checksum}");
}
