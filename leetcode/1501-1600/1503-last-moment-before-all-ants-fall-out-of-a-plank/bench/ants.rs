// LeetCode #1503: Last Moment Before All Ants Fall Out of a Plank -- the
// benchmark, the same algorithm as ants.kara: the statement simulated with
// doubled positions and half-unit ticks.

fn last_moment(n: i64, left: Vec<i64>, right: Vec<i64>) -> i64 {
    let mut pos: Vec<i64> = Vec::new();
    let mut dir: Vec<i64> = Vec::new();
    for &p in &left {
        pos.push(2 * p);
        dir.push(-1);
    }
    for &p in &right {
        pos.push(2 * p);
        dir.push(1);
    }
    let mut on = vec![true; pos.len()];
    let mut alive = pos.len();
    let mut at: Vec<i64> = vec![-1; (2 * n + 1) as usize];
    let (mut tick, mut last) = (0, 0);
    while alive > 0 {
        for i in 0..pos.len() {
            if on[i] && ((pos[i] == 0 && dir[i] == -1) || (pos[i] == 2 * n && dir[i] == 1)) {
                on[i] = false;
                alive -= 1;
                last = tick;
            }
        }
        for i in 0..pos.len() {
            if on[i] {
                let other = at[pos[i] as usize];
                if other >= 0 {
                    dir[i] = -dir[i];
                    dir[other as usize] = -dir[other as usize];
                } else {
                    at[pos[i] as usize] = i as i64;
                }
            }
        }
        for i in 0..pos.len() {
            if on[i] {
                at[pos[i] as usize] = -1;
                pos[i] += dir[i];
            }
        }
        tick += 1;
    }
    last / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_plank(most: i64, seed: &mut i64) -> (i64, Vec<i64>, Vec<i64>) {
    let n = next_random(seed) % most + 1;
    let fill = next_random(seed) % 100 + 1;
    let (mut left, mut right) = (Vec::new(), Vec::new());
    for p in 0..n + 1 {
        if next_random(seed) % 100 < fill {
            if next_random(seed) % 2 == 0 {
                left.push(p);
            } else {
                right.push(p);
            }
        }
    }
    (n, left, right)
}

fn main() {
    let mut seed = 1503;
    let planks: Vec<_> = (0..300).map(|_| random_plank(1000, &mut seed)).collect();
    let (mut total, mut check) = (0, 0);
    for (n, left, right) in &planks {
        let answer = last_moment(*n, left.clone(), right.clone());
        total += answer;
        check = mix(check, answer);
    }
    println!("300 planks of 1 to 1000 units simulated: sum {total}, checksum {check}");
}
