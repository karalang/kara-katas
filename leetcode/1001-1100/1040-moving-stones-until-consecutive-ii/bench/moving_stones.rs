// Benchmark lane for LeetCode 1040 -- Rust mirror of moving_stones.kara.

fn moves(stones: &[i64]) -> (i64, i64) {
    let mut s = stones.to_vec();
    s.sort();
    let n = s.len();
    let ni = n as i64;
    let most = (s[n - 1] - s[1] - ni + 2).max(s[n - 2] - s[0] - ni + 2);
    let mut least = ni;
    let mut i = 0usize;
    for j in 0..n {
        while s[j] - s[i] >= ni {
            i += 1;
        }
        let inside = (j - i + 1) as i64;
        if inside == ni - 1 && s[j] - s[i] == ni - 2 {
            least = least.min(2);
        } else {
            least = least.min(ni - inside);
        }
    }
    (least, most)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, top: i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    (a * 32768 + b) % top
}

fn main() {
    let count = 400;
    let size = 10000usize;
    let rounds = 5;
    let mut seed = 1040i64;
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let widest = if c % 2 == 0 { 100000 } else { 3 };
        let mut stones: Vec<i64> = Vec::with_capacity(size);
        let mut at = 0i64;
        for _ in 0..size {
            at += draw(&mut seed, widest) + 1;
            stones.push(at);
        }
        let mut i = size - 1;
        while i > 0 {
            let j = draw(&mut seed, i as i64 + 1) as usize;
            stones.swap(i, j);
            i -= 1;
        }
        sets.push(stones);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for stones in &sets {
            let (least, most) = moves(stones);
            total += least + most;
            check = (check * 131 + least * 1000003 + most) % 1000000007;
        }
    }
    println!("{} sets of {} stones, {} rounds: total {}, checksum {}", count, size, rounds, total, check);
}
