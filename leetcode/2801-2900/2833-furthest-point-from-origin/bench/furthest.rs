// LeetCode #2833: Furthest Point From Origin -- the bench, mirrored from
// furthest.kara: the L and R counts, and the blanks.

fn furthest_distance_from_origin(moves: &str) -> i64 {
    let left = moves.chars().filter(|&c| c == 'L').count() as i64;
    let right = moves.chars().filter(|&c| c == 'R').count() as i64;
    (left - right).abs() + moves.len() as i64 - left - right
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 100;
    let n = 50;
    let mut seed = 2833;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let blank = next_random(&mut seed) % 6;
        let codes: Vec<u8> = (0..n)
            .map(|_| {
                let r = next_random(&mut seed) % 6;
                if r < blank { b'_' } else if r % 2 == 0 { b'L' } else { b'R' }
            })
            .collect();
        strings.push(String::from_utf8(codes).unwrap());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for moves in strings.iter() {
            let d = furthest_distance_from_origin(moves);
            total += d;
            check = (check * 31 + d + r) % 1000000007;
        }
    }
    println!("{count} strings of {n}, {rounds} rounds: distances total {total}, checksum {check}");
}
