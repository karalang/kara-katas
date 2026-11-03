// Benchmark lane for LeetCode 1041 -- Rust mirror of robot_bounded.kara.

fn is_robot_bounded(instructions: &str) -> bool {
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    // north, east, south, west
    let mut facing: i64 = 0;
    for c in instructions.chars() {
        if c == 'G' {
            if facing == 0 {
                y += 1;
            } else if facing == 1 {
                x += 1;
            } else if facing == 2 {
                y -= 1;
            } else {
                x -= 1;
            }
        } else if c == 'L' {
            facing = (facing + 3) % 4;
        } else {
            facing = (facing + 1) % 4;
        }
    }
    (x == 0 && y == 0) || facing != 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, size, rounds) = (2000, 100, 500);
    let mut seed: i64 = 1041;
    let letters = ['G', 'L', 'R'];
    let mut strings: Vec<String> = Vec::new();
    for k in 0..count {
        let mut s = String::new();
        for _ in 0..size {
            let r = next_random(&mut seed) % 10;
            let c = if k % 2 == 0 {
                letters[(r % 3) as usize]
            } else if r < 8 {
                'G'
            } else if r == 8 {
                'L'
            } else {
                'R'
            };
            s.push(c);
        }
        strings.push(s);
    }
    let mut bounded: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in &strings {
            let answer = is_robot_bounded(s);
            if answer {
                bounded += 1;
            }
            check = (check * 131 + if answer { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("{count} strings of {size} instructions, {rounds} rounds: {bounded} bounded, checksum {check}");
}
