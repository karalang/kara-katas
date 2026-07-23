fn eval_rpn(tok: &[i64], stk: &mut [i64], modp: i64) -> i64 {
    let t = tok.len();
    let mut sp: usize = 0;
    for i in 0..t {
        let x = tok[i];
        if x >= 0 {
            stk[sp] = x;
            sp += 1;
        } else {
            let op = -x - 1;
            sp -= 1;
            let b = stk[sp];
            sp -= 1;
            let a = stk[sp];
            let r = if op == 0 {
                a + b
            } else if op == 1 {
                a - b
            } else if op == 2 {
                a * b
            } else {
                a / b
            };
            let r = ((r % modp) + modp) % modp;
            stk[sp] = r;
            sp += 1;
        }
    }
    stk[0]
}

fn main() {
    let m: i64 = 100000;
    let punches: i64 = 700;
    let modp: i64 = 1000000007;
    let opr: i64 = 1000;

    let mut tok: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;

    state = (state * 1103515245 + 12345) & 2147483647;
    tok.push(state % opr + 1);
    state = (state * 1103515245 + 12345) & 2147483647;
    tok.push(state % opr + 1);
    state = (state * 1103515245 + 12345) & 2147483647;
    tok.push(-(state % 4) - 1);

    let mut k = 2;
    while k <= m {
        state = (state * 1103515245 + 12345) & 2147483647;
        tok.push(state % opr + 1);
        state = (state * 1103515245 + 12345) & 2147483647;
        tok.push(-(state % 4) - 1);
        k += 1;
    }

    let mut stk = [0i64; 4];

    let mut sink: i64 = 0;
    for _pn in 0..punches {
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = state % (m + 1);
        let tokpos = if r == 0 { 0 } else { 2 * r - 1 } as usize;
        state = (state * 1103515245 + 12345) & 2147483647;
        tok[tokpos] = state % opr + 1;
        let res = eval_rpn(&tok, &mut stk, modp);
        sink = (sink + res) % modp;
    }
    println!("{}", sink);
}
