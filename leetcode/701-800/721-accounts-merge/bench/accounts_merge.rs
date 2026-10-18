// LeetCode #721: Accounts Merge -- union-find over the emails.
// Benchmark mirror of the Kara star arm: every email numbered the first
// time it is seen, each account's emails joined in a union-find, then the
// emails gathered by their root, each group sorted under its name.

use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find(parent: &mut Vec<usize>, x: usize) -> usize {
    let mut root = x;
    while parent[root] != root {
        root = parent[root];
    }
    let mut at = x;
    while parent[at] != root {
        let up = parent[at];
        parent[at] = root;
        at = up;
    }
    root
}

fn accounts_merge(accounts: &[Vec<String>]) -> Vec<Vec<String>> {
    let mut id: HashMap<String, usize> = HashMap::new();
    let mut emails: Vec<String> = Vec::new();
    let mut owner: Vec<String> = Vec::new();
    let mut parent: Vec<usize> = Vec::new();
    for account in accounts {
        let mut first: Option<usize> = None;
        for email in &account[1..] {
            if !id.contains_key(email) {
                id.insert(email.clone(), emails.len());
                parent.push(emails.len());
                emails.push(email.clone());
                owner.push(account[0].clone());
            }
            let e = id[email];
            match first {
                None => first = Some(e),
                Some(f) => {
                    let a = find(&mut parent, f);
                    let b = find(&mut parent, e);
                    if a != b {
                        parent[b] = a;
                    }
                }
            }
        }
    }
    let mut groups: HashMap<usize, Vec<String>> = HashMap::new();
    for e in 0..emails.len() {
        let root = find(&mut parent, e);
        groups.entry(root).or_default().push(emails[e].clone());
    }
    let mut merged: Vec<Vec<String>> = Vec::new();
    for (root, group) in &groups {
        let mut sorted = group.clone();
        sorted.sort();
        let mut account = vec![owner[*root].clone()];
        for email in &sorted {
            account.push(email.clone());
        }
        merged.push(account);
    }
    merged
}

fn main() {
    let names = ["Ada", "Bo", "Cy", "Di"];
    let mut seed: i64 = 721;
    let mut lists: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..20 {
        let mut accounts: Vec<Vec<String>> = Vec::new();
        for _ in 0..1000 {
            let who = next_random(&mut seed) % 4;
            let mut account = vec![names[who as usize].to_string()];
            let n = 1 + next_random(&mut seed) % 4;
            for _ in 0..n {
                let e = 4 * (next_random(&mut seed) % 2000) + who;
                account.push(format!("u{}@m.co", e));
            }
            accounts.push(account);
        }
        lists.push(accounts);
    }
    let mut sum = 0usize;
    for round in 0..50usize {
        for d in 0..20usize {
            let i = (round * 7919 + d * 104729) % 1000;
            let mut j = (i + 1) % 1000;
            while lists[d][j][0] != lists[d][i][0] {
                j = (j + 1) % 1000;
            }
            let last = lists[d][i].len() - 1;
            lists[d][i][last] = lists[d][j][1].clone();
            let merged = accounts_merge(&lists[d]);
            sum += merged.len();
            for person in &merged {
                sum += person[1].len();
            }
        }
    }
    println!("50 rounds of 20 lists of 1000 accounts: sum {}", sum);
}
