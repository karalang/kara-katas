// LeetCode #1056: Confusing Number -- the benchmark, mirror of confusing.kara.

fn confusing_number(n: i64) -> bool {
    let turned: [i64; 10] = [0, 1, -1, -1, -1, -1, 9, -1, 8, 6];
    let mut rest = n;
    let mut upside = 0;
    while rest > 0 {
        let d = turned[(rest % 10) as usize];
        if d < 0 {
            return false;
        }
        upside = upside * 10 + d;
        rest /= 10;
    }
    upside != n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 500000;
    let rounds = 20;
    let turning: [i64; 5] = [0, 1, 6, 8, 9];
    let other: [i64; 5] = [2, 3, 4, 5, 7];
    let mut seed = 1056;
    let mut numbers: Vec<i64> = Vec::new();
    for _ in 0..count {
        let digits = 6 + next_random(&mut seed) % 5;
        let spoiled = if next_random(&mut seed) % 8 == 0 { next_random(&mut seed) % digits } else { -1 };
        let mut n = turning[(1 + next_random(&mut seed) % 4) as usize];
        for k in 1..digits {
            let d = if k == spoiled {
                other[(next_random(&mut seed) % 5) as usize]
            } else {
                turning[(next_random(&mut seed) % 5) as usize]
            };
            n = n * 10 + d;
        }
        numbers.push(n);
    }
    let mut total = 0;
    let mut check = 0;
    for _ in 0..rounds {
        let mut found = 0;
        for &n in numbers.iter() {
            if confusing_number(n) {
                found += 1;
                check = (check + n % 1000) % 1000000007;
            }
        }
        total += found;
        check = (check * 131 + found) % 1000000007;
    }
    println!("{count} numbers, {rounds} rounds: {total} confusing, checksum {check}");
}
