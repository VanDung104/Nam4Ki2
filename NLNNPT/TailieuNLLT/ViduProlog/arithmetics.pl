%%[swi('demo/likes')].
%%[swi('demo/loves')].
%%[swi('doc/packages/examples/cpp/likes')].
%%[swi('D:/Prolog/examples/loves')].
%%['D:/Prolog/examples/loves'].
%%[swi('D:\\Prolog\\examples\\loves')].

%%['D:/Prolog/examples/arithmetics'].

% factorial(N, F) :- F is N!.
factorial(0, 1).
factorial(N, F) :- N > 0, N1 is N-1, factorial(N1, F1), F is N*F1.

% length(Xs, N):- N is the length of the list Xs.
lengths([], 0).
lengths([_| Ts], N) :- lengths(Ts, M), N is M+1.

%part( , [], [], []).
%part(X, [Y | Xs], [Y | Ls], Bs) :-X>Y,!, part(X, Xs, Ls, Bs).
%part(X, [Y | Xs], Ls, [Y | Bs]) :- part(X, Xs, Ls, Bs).


