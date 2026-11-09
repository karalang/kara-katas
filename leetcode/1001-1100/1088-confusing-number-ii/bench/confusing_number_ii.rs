// Benchmark: LeetCode #1088 Confusing Number II -- mirrors
// confusing_number_ii.kara: a depth-first walk over the numbers made of the
// digits that rotate, each carrying its rotation, for 400 random n up to
// 10^9 drawn once.

fn rotated(d: i64) -> i64 {
    match d {
        0 => 0,
        1 => 1,
        6 => 9,
        8 => 8,
        9 => 6,
        _ => -1,
    }
}

fn count_from(num: i64, rot: i64, unit: i64, n: i64) -> i64 {
    let mut total = 0;
    for d in [0, 1, 6, 8, 9] {
        let next = num * 10 + d;
        if next > n {
            break;
        }
        if next == 0 {
            continue;
        }
        let r = rotated(d) * unit + rot;
        if next != r {
            total += 1;
        }
        total += count_from(next, r, unit * 10, n);
    }
    total
}

fn confusing_number_ii(n: i64) -> i64 {
    count_from(0, 0, 1, n)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1088;
    let mut ns: Vec<i64> = Vec::new();
    for _ in 0..400 {
        let a = next_random(&mut seed);
        let hi = a * 32768 + next_random(&mut seed);
        ns.push(hi % 1000000000 + 1);
    }
    let mut total = 0;
    let mut check = 0;
    for &n in ns.iter() {
        let a = confusing_number_ii(n);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("400 n up to 10^9: {} confusing numbers, checksum {}", total, check);
}
