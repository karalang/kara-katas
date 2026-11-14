// LeetCode #2147: Number of Ways to Divide a Long Corridor -- the
// benchmark's Rust mirror of corridor.kara.

const MOD: i64 = 1000000007;

fn number_of_ways(corridor: &str) -> i64 {
    let seats: Vec<i64> = corridor
        .chars()
        .enumerate()
        .filter(|&(_, ch)| ch == 'S')
        .map(|(i, _)| i as i64)
        .collect();
    if seats.is_empty() || seats.len() % 2 == 1 {
        return 0;
    }
    let mut ways = 1;
    for p in (2..seats.len()).step_by(2) {
        ways = ways * (seats[p] - seats[p - 1]) % MOD;
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2147;
    let mut corridors: Vec<String> = Vec::new();
    for _ in 0..4 {
        let mut corridor = String::new();
        let mut count = 0;
        for _ in 0..99999 {
            if next_random(&mut seed) % 3 == 0 {
                corridor.push('S');
                count += 1;
            } else {
                corridor.push('P');
            }
        }
        corridor.push(if count % 2 == 1 { 'S' } else { 'P' });
        corridors.push(corridor);
    }
    let mut total = 0;
    let mut check = 0;
    for round in 0..25 {
        for c in 0..4 {
            let i = (next_random(&mut seed) % 99999) as usize;
            let place = corridors[c].clone();
            corridors[c] = format!("{}{}{}{}", &place[..i], &place[i + 1..i + 2], &place[i..i + 1], &place[i + 2..]);
            let ways = number_of_ways(&corridors[c]);
            total = (total + ways) % MOD;
            check = (check * 31 + ways + round) % MOD;
        }
    }
    println!("100 counts: {} ways in all, checksum {}", total, check);
}
