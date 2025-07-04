fib_tail(N, Result) :- fib_helper(N, 0, 1, Result).

fib_helper(0, A, _, A).
fib_helper(N, A, B, Result) :-
    N > 0,
    N1 is N - 1,
    Next is A + B,
    fib_helper(N1, B, Next, Result).
