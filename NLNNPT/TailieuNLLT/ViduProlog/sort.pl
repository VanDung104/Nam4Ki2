%%[swi('demo/likes')].
%%[swi('demo/loves')].
%%[swi('doc/packages/examples/cpp/likes')].
%%[swi('D:/Prolog/examples/loves')].
%%['D:/Prolog/examples/loves'].
%%[swi('D:\\Prolog\\examples\\loves')].

%%['D:/Prolog/examples/sort'].

% ordered(Xs) :- Xs is an =<-ordered list of numbers
ordered([]).
ordered([_]).
ordered([X, Y | Xs]) :- X =< Y, ordered([Y | Xs]).

% qs(Xs, Ys):- Ys is an ordered permutation of the list Xs.
qs([], []).
qs([X | Xs], Ys):-
part(X, Xs, Littles, Bigs),
qs(Littles, Ls),
qs(Bigs, Bs),
append(Ls, [X | Bs], Ys).
% part(X, Xs, Ls, Bs):- Ls is a list of elements of Xs which are < X,
% Bs is a list of elements of Xs which are >= X.
part(_, [], [], []).
part(X, [Y | Xs], [Y | Ls], Bs) :-X>Y, part(X, Xs, Ls, Bs).
part(X, [Y | Xs], Ls, [Y | Bs]) :- X =< Y, part(X, Xs, Ls, Bs).

% qs(Xs, Ys) :- Ys is an ordered permutation of the list Xs.

qs_n(Xs, Ys) :- qs_dl(Xs, Ys - []).

%qs_dl(Xs, Y) :- Y is a difference list representing the
% ordered permutation of the list Xs.
qs_dl([], Xs - Xs).
qs_dl([X | Xs], Ys - Zs) :-
part(X, Xs, Littles, Bigs),
qs_dl(Littles, Ys - [X | Y1s]),
qs_dl(Bigs, Y1s - Zs).



