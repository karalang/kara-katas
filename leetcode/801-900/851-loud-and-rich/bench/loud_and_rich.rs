// Benchmark for #851: Loud and Rich -- Rust twin of the Kāra ★ arm
// (memoised search up the richer-than graph).

fn answer_for(x: usize, richer_than: &[Vec<usize>], quiet: &[i64], answer: &mut Vec<i64>) -> usize {
    if answer[x] < 0 {
        let mut best = x;
        for &y in richer_than[x].iter() {
            let candidate = answer_for(y, richer_than, quiet, answer);
            if quiet[candidate] < quiet[best] {
                best = candidate;
            }
        }
        answer[x] = best as i64;
    }
    answer[x] as usize
}

fn loud_and_rich(richer: &[[usize; 2]], quiet: &[i64]) -> Vec<i64> {
    let n = quiet.len();
    let mut richer_than: Vec<Vec<usize>> = Vec::new();
    for _ in 0..n {
        richer_than.push(Vec::new());
    }
    for pair in richer.iter() {
        richer_than[pair[1]].push(pair[0]);
    }
    let mut answer: Vec<i64> = vec![-1; n];
    for x in 0..n {
        let _ = answer_for(x, &richer_than, quiet, &mut answer);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 10000;
    let n: usize = 500;
    let mut seed: i64 = 851;
    let mut cases: Vec<(Vec<[usize; 2]>, Vec<i64>)> = Vec::new();
    for g in 0..count {
        let odds = 2i64 << (g % 8);
        let mut rank: Vec<usize> = (0..n).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            rank.swap(i, j);
        }
        let mut richer: Vec<[usize; 2]> = Vec::new();
        for i in 0..n {
            for j in i + 1..n {
                if next_random(&mut seed) % 1000 < odds {
                    richer.push([rank[i], rank[j]]);
                }
            }
        }
        let mut quiet: Vec<i64> = (0..n as i64).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            quiet.swap(i, j);
        }
        cases.push((richer, quiet));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let (richer, quiet) = &cases[round % count];
        let answer = loud_and_rich(richer, quiet);
        for &a in answer.iter() {
            total += quiet[a as usize];
            checksum = (checksum * 31 + a) % 1000000007;
        }
    }
    println!("{} rounds of {} cases: quietness sums to {}, checksum {}", rounds, count, total, checksum);
}
