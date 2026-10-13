// Benchmark for #473: Rust mirror of the ★ arm (backtracking, longest
// stick first); see matchsticks.kara.

fn place(sticks: &[i64], i: usize, sides: &mut [i64; 4], side: i64) -> bool {
    if i == sticks.len() {
        return true;
    }
    for s in 0..4 {
        if sides[s] + sticks[i] > side {
            continue;
        }
        let mut repeat = false;
        for t in 0..s {
            if sides[t] == sides[s] {
                repeat = true;
                break;
            }
        }
        if repeat {
            continue;
        }
        sides[s] += sticks[i];
        if place(sticks, i + 1, sides, side) {
            return true;
        }
        sides[s] -= sticks[i];
    }
    false
}

fn makesquare(matchsticks: &[i64]) -> bool {
    if matchsticks.len() < 4 {
        return false;
    }
    let mut total = 0;
    for m in matchsticks {
        total += m;
    }
    if total % 4 != 0 {
        return false;
    }
    let side = total / 4;
    let mut sticks = matchsticks.to_vec();
    sticks.sort();
    sticks.reverse();
    if sticks[0] > side {
        return false;
    }
    let mut sides = [0i64; 4];
    place(&sticks, 0, &mut sides, side)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let cases = 2000;
    let mut seed: i64 = 473;
    let mut squares = 0;
    let mut checksum: i64 = 0;
    for _ in 0..cases {
        let mut sticks: Vec<i64> = Vec::new();
        let mut total = 0;
        for _ in 0..15 {
            let v = 50 + next_random(&mut seed) % 50;
            sticks.push(v);
            total += v;
        }
        sticks[14] += (4 - total % 4) % 4;
        let ok = makesquare(&sticks);
        if ok {
            squares += 1;
        }
        checksum = (checksum * 3 + if ok { 1 } else { 2 }) % 1000000007;
    }
    println!("{} sets of 15 sticks: {} squares, checksum {}", cases, squares, checksum);
}
