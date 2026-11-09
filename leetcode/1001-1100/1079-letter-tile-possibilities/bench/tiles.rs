// LeetCode #1079 bench: the Rust mirror of tiles.kara, the same walk
// over an [i64; 26] of counts and the same workload.

fn sequences(counts: &mut [i64; 26]) -> i64 {
    let mut total = 0;
    for letter in 0..26 {
        if counts[letter] > 0 {
            counts[letter] -= 1;
            total += 1 + sequences(counts);
            counts[letter] += 1;
        }
    }
    total
}

fn num_tile_possibilities(tiles: &str) -> i64 {
    let mut counts = [0i64; 26];
    for b in tiles.bytes() {
        counts[(b - b'A') as usize] += 1;
    }
    sequences(&mut counts)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 200;
    let mut seed = 1079;
    let mut sets: Vec<String> = Vec::new();
    for _ in 0..200 {
        let d = next_random(&mut seed) % 7 + 1;
        let mut alphabet: Vec<u8> = Vec::new();
        while (alphabet.len() as i64) < d {
            let c = b'A' + (next_random(&mut seed) % 26) as u8;
            if !alphabet.contains(&c) {
                alphabet.push(c);
            }
        }
        let mut tiles = String::new();
        for _ in 0..7 {
            tiles.push(alphabet[(next_random(&mut seed) % d) as usize] as char);
        }
        sets.push(tiles);
    }
    let n = sets.len();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for j in 0..n {
            let count = num_tile_possibilities(&sets[(j * 7 + r) % n]);
            total += count;
            check = (check * 31 + count) % 1000000007;
        }
    }
    println!("{} rounds of {} sets of 7 tiles: {} sequences, checksum {}", rounds, n, total, check);
}
