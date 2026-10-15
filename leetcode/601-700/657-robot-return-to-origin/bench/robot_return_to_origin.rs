// Benchmark for #657: walk the moves, as the Kara ★ arm.

fn judge_circle(moves: &str) -> bool {
    let mut x = 0i64;
    let mut y = 0i64;
    for m in moves.chars() {
        match m {
            'U' => y += 1,
            'D' => y -= 1,
            'L' => x -= 1,
            _ => x += 1,
        }
    }
    x == 0 && y == 0
}

fn main() {
    let inputs = 8i64;
    let rounds = 100i64;
    let mut seed: i64 = 657;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let letters = ['U', 'D', 'L', 'R'];
    let mut strings: Vec<String> = Vec::new();
    for k in 0..inputs {
        let n = 1000000i64;
        let mut steps: Vec<char> = Vec::with_capacity(n as usize);
        if k % 2 == 0 {
            for _ in 0..n / 2 {
                let pair = (next_random() % 2) as usize;
                steps.push(letters[pair * 2]);
                steps.push(letters[pair * 2 + 1]);
            }
            let mut i = steps.len() as i64 - 1;
            while i > 0 {
                let j = next_random() % (i + 1);
                steps.swap(i as usize, j as usize);
                i -= 1;
            }
        } else {
            for _ in 0..n {
                steps.push(letters[(next_random() % 4) as usize]);
            }
        }
        strings.push(steps.into_iter().collect());
    }
    let mut back = 0i64;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let pick = (r * 3) % inputs;
        let at = judge_circle(&strings[pick as usize]);
        if at {
            back += 1;
        }
        checksum = (checksum * 31 + pick * 2 + if at { 1 } else { 0 }) % 1000000007;
    }
    println!("{} strings of 1000000, {} rounds: {} back, checksum {}", inputs, rounds, back, checksum);
}
