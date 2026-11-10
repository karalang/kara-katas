// LeetCode #2092: Find All People With Secret -- Rust mirror of the ★ arm's
// benchmark (secret.kara): the same 10 gatherings, each answered 4 times by
// the same sort and union-find over `Vec`s.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut x = x;
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn find_all_people(n: usize, meetings: &[(usize, usize, i64)], first_person: usize) -> Vec<usize> {
    let mut sorted = meetings.to_vec();
    sorted.sort_by_key(|&(_, _, t)| t);
    let mut parent: Vec<usize> = (0..n).collect();
    parent[first_person] = 0;
    let mut i = 0;
    while i < sorted.len() {
        let mut j = i;
        while j < sorted.len() && sorted[j].2 == sorted[i].2 {
            let (x, y, _) = sorted[j];
            let (rx, ry) = (find(&mut parent, x), find(&mut parent, y));
            if rx < ry {
                parent[ry] = rx;
            } else {
                parent[rx] = ry;
            }
            j += 1;
        }
        for k in i..j {
            let (x, y, _) = sorted[k];
            if find(&mut parent, x) != 0 {
                parent[x] = x;
            }
            if find(&mut parent, y) != 0 {
                parent[y] = y;
            }
        }
        i = j;
    }
    let mut knows = Vec::new();
    for p in 0..n {
        if find(&mut parent, p) == 0 {
            knows.push(p);
        }
    }
    knows
}

fn main() {
    let mut seed = 2092i64;
    let n = 100000i64;
    let mut gatherings: Vec<Vec<(usize, usize, i64)>> = Vec::new();
    for _ in 0..10 {
        let mut meetings = Vec::new();
        for _ in 0..100000 {
            let x = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let y = (x + 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 1)) % n;
            meetings.push((x as usize, y as usize, next_random(&mut seed) % 1000 + 1));
        }
        gatherings.push(meetings);
    }
    let (mut total, mut check) = (0usize, 0i64);
    for round in 0..4 {
        for g in 0..10 {
            let got = find_all_people(n as usize, &gatherings[g], round * 10 + g + 1);
            total += got.len();
            for &p in &got {
                check = (check * 31 + p as i64) % 1000000007;
            }
        }
    }
    println!("40 answers: {} people, checksum {}", total, check);
}
