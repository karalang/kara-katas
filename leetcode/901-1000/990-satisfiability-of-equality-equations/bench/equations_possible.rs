// LeetCode #990: Satisfiability of Equality Equations -- bench, the ★
// arm (union-find with path halving), the same algorithm and workload
// as equations_possible.kara.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut at = x;
    while parent[at as usize] != at {
        parent[at as usize] = parent[parent[at as usize] as usize];
        at = parent[at as usize];
    }
    at
}

fn equations_possible(equations: &[String]) -> bool {
    let mut parent: Vec<i64> = (0..26).collect();
    for e in equations {
        let b = e.as_bytes();
        if b[1] == b'=' {
            let x = find(&mut parent, b[0] as i64 - 97);
            let y = find(&mut parent, b[3] as i64 - 97);
            parent[x as usize] = y;
        }
    }
    for e in equations {
        let b = e.as_bytes();
        if b[1] == b'!' && find(&mut parent, b[0] as i64 - 97) == find(&mut parent, b[3] as i64 - 97) {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(i: i64) -> String {
    ((97 + i) as u8 as char).to_string()
}

fn random_equations(n: usize, unequal: i64, seed: &mut i64) -> Vec<String> {
    let mut out = Vec::new();
    for _ in 0..n {
        let a = letter(next_random(seed) % 26);
        let op = if next_random(seed) % 256 < unequal { "!=" } else { "==" };
        let b = letter(next_random(seed) % 26);
        out.push(a + op + &b);
    }
    out
}

fn main() {
    let rounds = 6000;
    let mut seed = 990;
    let sets: Vec<Vec<String>> = (0..20).map(|i| random_equations(500, i % 2, &mut seed)).collect();
    let mut sat = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let ok = equations_possible(&sets[(r + i) % 20]);
            if ok {
                sat += 1;
            }
            check = (check * 31 + if ok { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("{} rounds over 20 sets of 500 equations: {} satisfiable, checksum {}", rounds, sat, check);
}
