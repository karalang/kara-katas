// Benchmark for #433: mirror of min_mutation.kara (breadth first,
// generating neighbours). std's HashSet hashes with SipHash-1-3 under a
// random key, as Kāra's Set does.
use std::collections::HashSet;

fn min_mutation(start_gene: &str, end_gene: &str, bank: &[String]) -> i64 {
    let mut unreached: HashSet<String> = HashSet::new();
    for gene in bank {
        unreached.insert(gene.clone());
    }
    if !unreached.contains(end_gene) {
        return -1;
    }
    unreached.remove(start_gene);
    let mut level: Vec<String> = vec![start_gene.to_string()];
    let mut steps = 0;
    while !level.is_empty() {
        let mut next: Vec<String> = Vec::new();
        for gene in &level {
            if gene == end_gene {
                return steps;
            }
            let letters: Vec<char> = gene.chars().collect();
            for i in 0..letters.len() {
                for c in ['A', 'C', 'G', 'T'] {
                    if c != letters[i] {
                        let mut mutant = String::new();
                        for j in 0..letters.len() {
                            mutant.push(if j == i { c } else { letters[j] });
                        }
                        if unreached.remove(&mutant) {
                            next.push(mutant);
                        }
                    }
                }
            }
        }
        level = next;
        steps += 1;
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mutate(gene: &str, seed: &mut i64) -> String {
    let at = next_random(seed) % 8;
    let shift = 1 + next_random(seed) % 3;
    let letters = ['A', 'C', 'G', 'T'];
    let mut out = String::new();
    for (i, c) in gene.chars().enumerate() {
        if i as i64 == at {
            let k = match c {
                'A' => 0,
                'C' => 1,
                'G' => 2,
                _ => 3,
            };
            out.push(letters[((k + shift) % 4) as usize]);
        } else {
            out.push(c);
        }
    }
    out
}

fn main() {
    let size: usize = 1000;
    let searches: i64 = std::env::args().nth(1).map_or(2000, |a| a.parse().unwrap());
    let mut seed: i64 = 433;
    let mut bank: Vec<String> = vec!["ACGTACGT".to_string()];
    while bank.len() < size {
        let parent = bank[(next_random(&mut seed) % bank.len() as i64) as usize].clone();
        bank.push(mutate(&parent, &mut seed));
    }
    let mut reachable = 0;
    let mut checksum: i64 = 0;
    for _ in 0..searches {
        let start = mutate(&bank[(next_random(&mut seed) % size as i64) as usize], &mut seed);
        let end = bank[(next_random(&mut seed) % size as i64) as usize].clone();
        let answer = min_mutation(&start, &end, &bank);
        if answer >= 0 {
            reachable += 1;
        }
        checksum = (checksum * 31 + answer + 2) % 1000000007;
    }
    println!("{} searches in a bank of {}: {} reachable, checksum {}", searches, size, reachable, checksum);
}
