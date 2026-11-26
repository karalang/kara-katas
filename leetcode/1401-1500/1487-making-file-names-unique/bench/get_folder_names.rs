// LeetCode #1487: Making File Names Unique -- bench, the Rust twin of
// get_folder_names.kara.
use std::collections::HashMap;

fn get_folder_names(names: &[String]) -> Vec<String> {
    let mut next: HashMap<String, i64> = HashMap::new();
    let mut out: Vec<String> = Vec::new();
    for name in names {
        match next.get(name) {
            None => {
                next.insert(name.clone(), 1);
                out.push(name.clone());
            }
            Some(&from) => {
                let mut k = from;
                while next.contains_key(&format!("{}({})", name, k)) {
                    k += 1;
                }
                let made = format!("{}({})", name, k);
                next.insert(name.clone(), k + 1);
                next.insert(made.clone(), 1);
                out.push(made);
            }
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn name_of(b: i64, suffix: i64) -> String {
    let base = format!("{}{}", (b'a' + (b % 26) as u8) as char, b / 26);
    if suffix == 0 { base } else { format!("{}({})", base, suffix) }
}

fn main() {
    let mut seed: i64 = 1487;
    let mut names: Vec<String> = Vec::new();
    for _ in 0..50000 {
        let b = next_random(&mut seed) % 3000;
        let s = next_random(&mut seed) % 9;
        names.push(name_of(b, if s < 3 { s + 1 } else { 0 }));
    }
    let mut check: i64 = 0;
    for pass in 0..20i64 {
        names[(check % 50000) as usize] = name_of(check % 3000, check % 4);
        let folders = get_folder_names(&names);
        for f in &folders {
            for &b in f.as_bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
        check = (check + pass) % 1000000007;
    }
    println!("20 passes over 50000 names: checksum {}", check);
}
