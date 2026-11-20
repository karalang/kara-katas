// LeetCode #1202 bench, in Rust: the ★ arm (a union-find over the indices,
// path halving and union by size; each group's letters, sorted, go back to
// its indices in rising order) on one string of 100000 random letters and
// four sets of pairs drawn once, then 10 rounds over the four, each answer
// folded into a checksum.

fn find(parent: &mut [usize], mut x: usize) -> usize {
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn smallest_string_with_swaps(s: &[u8], pairs: &[[usize; 2]]) -> Vec<u8> {
    let n = s.len();
    let mut parent: Vec<usize> = (0..n).collect();
    let mut size = vec![1usize; n];
    for p in pairs {
        let mut a = find(&mut parent, p[0]);
        let mut b = find(&mut parent, p[1]);
        if a != b {
            if size[a] < size[b] {
                std::mem::swap(&mut a, &mut b);
            }
            parent[b] = a;
            size[a] += size[b];
        }
    }
    let mut groups: Vec<Vec<usize>> = vec![Vec::new(); n];
    for i in 0..n {
        let r = find(&mut parent, i);
        groups[r].push(i);
    }
    let mut out = s.to_vec();
    for g in &groups {
        let mut letters: Vec<u8> = g.iter().map(|&i| s[i]).collect();
        letters.sort();
        for k in 0..g.len() {
            out[g[k]] = letters[k];
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_pairs(seed: &mut i64, n: usize, m: usize) -> Vec<[usize; 2]> {
    let mut pairs = Vec::new();
    for _ in 0..m {
        let hi = next_random(seed);
        let a = ((hi * 32768 + next_random(seed)) as usize) % n;
        let hi = next_random(seed);
        let b = ((hi * 32768 + next_random(seed)) as usize) % n;
        pairs.push([a, b]);
    }
    pairs
}

fn main() {
    let n = 100000;
    let mut seed = 1202i64;
    let s: Vec<u8> = (0..n).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
    let sets = [
        random_pairs(&mut seed, n, 25000),
        random_pairs(&mut seed, n, 100000),
        (0..n - 2).map(|i| [i, i + 2]).collect(),
        (0..n - 1000).map(|i| [i, i + 1000]).collect(),
    ];
    let mut check: i64 = 0;
    for _ in 0..10 {
        for pairs in &sets {
            let t = smallest_string_with_swaps(&s, pairs);
            for &b in &t {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("10 rounds over 4 sets of pairs on 100000 letters: checksum {check}");
}
