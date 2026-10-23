// LeetCode #913: Cat and Mouse -- bench: Rust mirror of the retrograde
// analysis with a queue in cat_mouse_game.kara.

fn cat_mouse_game(graph: &[Vec<i64>]) -> i64 {
    let n = graph.len() as i64;
    let mut result = vec![0i64; (n * n * 2) as usize];
    let mut left = vec![0i64; (n * n * 2) as usize];
    for m in 0..n {
        for c in 1..n {
            left[((m * n + c) * 2) as usize] = graph[m as usize].len() as i64;
            let mut moves = 0;
            for &d in &graph[c as usize] {
                if d != 0 {
                    moves += 1;
                }
            }
            left[((m * n + c) * 2 + 1) as usize] = moves;
        }
    }
    let mut queue: Vec<i64> = Vec::new();
    for c in 1..n {
        for t in 0..2 {
            result[(c * 2 + t) as usize] = 1;
            queue.push(c * 2 + t);
            result[((c * n + c) * 2 + t) as usize] = 2;
            queue.push((c * n + c) * 2 + t);
        }
    }
    let mut head = 0;
    while head < queue.len() {
        let s = queue[head];
        head += 1;
        let t = s % 2;
        let c = s / 2 % n;
        let m = s / 2 / n;
        let won = result[s as usize];
        if t == 1 {
            for &pm in &graph[m as usize] {
                let p = ((pm * n + c) * 2) as usize;
                if result[p] == 0 {
                    if won == 1 {
                        result[p] = 1;
                        queue.push(p as i64);
                    } else {
                        left[p] -= 1;
                        if left[p] == 0 {
                            result[p] = 2;
                            queue.push(p as i64);
                        }
                    }
                }
            }
        } else {
            for &pc in &graph[c as usize] {
                if pc != 0 {
                    let p = ((m * n + pc) * 2 + 1) as usize;
                    if result[p] == 0 {
                        if won == 2 {
                            result[p] = 2;
                            queue.push(p as i64);
                        } else {
                            left[p] -= 1;
                            if left[p] == 0 {
                                result[p] = 1;
                                queue.push(p as i64);
                            }
                        }
                    }
                }
            }
        }
    }
    result[((n + 2) * 2) as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_graph(seed: &mut i64, n: i64, per: i64) -> Vec<Vec<i64>> {
    let nu = n as usize;
    let mut adj = vec![false; nu * nu];
    for u in 0..nu {
        for v in u + 1..nu {
            let chance = if u == 0 { per / 4 } else { per };
            if next_random(seed) % 1000 < chance {
                adj[u * nu + v] = true;
                adj[v * nu + u] = true;
            }
        }
    }
    for v in 1..nu {
        let mut alone = true;
        for u in 1..nu {
            if adj[v * nu + u] {
                alone = false;
            }
        }
        if alone {
            let mut u = (1 + next_random(seed) % (n - 2)) as usize;
            if u >= v {
                u += 1;
            }
            adj[u * nu + v] = true;
            adj[v * nu + u] = true;
        }
    }
    let mut hole_alone = true;
    for u in 1..nu {
        if adj[u] {
            hole_alone = false;
        }
    }
    if hole_alone {
        let u = (1 + next_random(seed) % (n - 1)) as usize;
        adj[u] = true;
        adj[u * nu] = true;
    }
    let mut graph: Vec<Vec<i64>> = Vec::new();
    for v in 0..nu {
        let mut near: Vec<i64> = Vec::new();
        for u in 0..nu {
            if adj[v * nu + u] {
                near.push(u as i64);
            }
        }
        graph.push(near);
    }
    graph
}

fn main() {
    let rounds = 4000;
    let mut seed = 913;
    let mut wins = [0i64; 3];
    let mut check = 0i64;
    for r in 0..rounds {
        let per = if r % 4 == 0 {
            20
        } else if r % 4 == 1 {
            60
        } else if r % 4 == 2 {
            150
        } else {
            400
        };
        let outcome = cat_mouse_game(&random_graph(&mut seed, 50, per));
        wins[outcome as usize] += 1;
        check = (check * 7 + outcome) % 1000000007;
    }
    println!(
        "{} graphs of 50 nodes: {} draws, {} mouse wins, {} cat wins, checksum {}",
        rounds, wins[0], wins[1], wins[2], check
    );
}
