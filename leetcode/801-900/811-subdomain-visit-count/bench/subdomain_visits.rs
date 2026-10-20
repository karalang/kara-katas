// LeetCode 811 -- Subdomain Visit Count: the bench, with the ★ arm's map
// from domain to visits.
use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn subdomain_visits(cpdomains: &[String]) -> Vec<String> {
    let mut counts: HashMap<String, i64> = HashMap::new();
    for entry in cpdomains {
        let space = entry.find(' ').unwrap();
        let n: i64 = entry[..space].parse().unwrap();
        let mut domain = &entry[space + 1..];
        loop {
            *counts.entry(domain.to_string()).or_insert(0) += n;
            match domain.find('.') {
                Some(dot) => domain = &domain[dot + 1..],
                None => break,
            }
        }
    }
    let mut out = Vec::new();
    for (domain, total) in counts {
        out.push(format!("{} {}", total, domain));
    }
    out
}

// A domain of 2 or 3 parts: a left part one time in three, then a middle
// part and a top part.
fn random_domain(seed: &mut i64) -> String {
    let tops = ["com", "org", "net", "io"];
    let middles = ["leetcode", "google", "yahoo", "wiki", "kara"];
    let lefts = ["mail", "discuss", "www", "api", "m", "docs"];
    let top = tops[(next_random(seed) % 4) as usize];
    let middle = middles[(next_random(seed) % 5) as usize];
    if next_random(seed) % 3 == 0 {
        format!("{}.{}", middle, top)
    } else {
        format!("{}.{}.{}", lefts[(next_random(seed) % 6) as usize], middle, top)
    }
}

// 64 lists of 100 entries are made once. Each round writes a new count
// into one entry of the next list and counts that list's visits; the
// answer's lines, in whatever order they come, are folded into a sum.
fn main() {
    let mut seed = 811;
    let mut lists: Vec<Vec<String>> = Vec::new();
    let mut domains: Vec<Vec<String>> = Vec::new();
    for _ in 0..64 {
        let mut list = Vec::new();
        let mut doms = Vec::new();
        for _ in 0..100 {
            let d = random_domain(&mut seed);
            list.push(format!("{} {}", 1 + next_random(&mut seed) % 10000, d));
            doms.push(d);
        }
        lists.push(list);
        domains.push(doms);
    }
    let rounds: i64 = 100000;
    let mut lines: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let k = (r % 64) as usize;
        let i = (r / 64 % 100) as usize;
        lists[k][i] = format!("{} {}", 1 + next_random(&mut seed) % 10000, domains[k][i]);
        let out = subdomain_visits(&lists[k]);
        let mut sum: i64 = 0;
        for line in &out {
            let space = line.find(' ').unwrap();
            sum += line[..space].parse::<i64>().unwrap() * 7 + line.len() as i64;
        }
        lines += out.len() as i64;
        check = (check * 131 + sum) % 1000000007;
    }
    println!("{} rounds of 100 entries: {} lines, checksum {}", rounds, lines, check);
}
