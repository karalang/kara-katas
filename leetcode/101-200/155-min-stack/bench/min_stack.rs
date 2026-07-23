struct MinStack {
    data: Vec<i64>,
    mins: Vec<i64>,
}

fn ms_new() -> MinStack {
    MinStack { data: Vec::new(), mins: Vec::new() }
}

fn ms_push(st: &mut MinStack, x: i64) {
    st.data.push(x);
    let m = st.mins.len();
    if m == 0 || x <= st.mins[m - 1] {
        st.mins.push(x);
    } else {
        st.mins.push(st.mins[m - 1]);
    }
}

fn ms_pop(st: &mut MinStack) {
    st.data.pop();
    st.mins.pop();
}

fn ms_top(st: &MinStack) -> i64 {
    st.data[st.data.len() - 1]
}

fn ms_get_min(st: &MinStack) -> i64 {
    st.mins[st.mins.len() - 1]
}

fn main() {
    let ops: i64 = 90000000;
    let cap: i64 = 100000;

    let mut st = ms_new();
    let mut state: i64 = 12345;
    let mut sz: i64 = 0;
    let mut sink: i64 = 0;

    for _i in 0..ops {
        state = (state * 1103515245 + 12345) & 2147483647;
        let op = (state / 1024) % 4;
        if sz == 0 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let val = state % 2000000 - 1000000;
            ms_push(&mut st, val);
            sz += 1;
        } else if sz >= cap {
            ms_pop(&mut st);
            sz -= 1;
        } else if op == 0 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let val = state % 2000000 - 1000000;
            ms_push(&mut st, val);
            sz += 1;
        } else if op == 1 {
            ms_pop(&mut st);
            sz -= 1;
        } else if op == 2 {
            sink += ms_get_min(&st);
        } else {
            sink += ms_top(&st);
        }
    }
    println!("{}", sink);
}
