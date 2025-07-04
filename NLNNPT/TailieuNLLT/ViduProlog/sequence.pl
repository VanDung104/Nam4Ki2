%%[swi('demo/likes')].
%%[swi('demo/loves')].
%%[swi('doc/packages/examples/cpp/likes')].
%%[swi('D:/Prolog/examples/loves')].
%%['D:/Prolog/examples/loves'].
%%[swi('D:\\Prolog\\examples\\loves')].

%%['D:/Prolog/examples/sequence'].

% append(Xs, Ys, Zs) :- Zs is the result of concatenating the lists Xs and Ys.

append([], Ys, Ys).
append([X | Xs], Ys, [X | Zs]) :- append(Xs, Ys, Zs).

% sublist(Xs, Ys) :- Xs sublist of Ys

sublist(Xs, Ys) :- append(_, Zs, Ys), append(Xs,_, Zs).

% sequence(Xs) :- Xs is a list of 27 variables.
sequence([_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_]).
% question(Ss) :- Ss is a solution to the problem.
question(Ss) :-
sequence(Ss),
sublist([9,_,_,_,_,_,_,_,_,_,9,_,_,_,_,_,_,_,_,_,9], Ss),
sublist([8,_,_,_,_,_,_,_,_,8,_,_,_,_,_,_,_,_,8], Ss),
sublist([7,_,_,_,_,_,_,_,7,_,_,_,_,_,_,_,7], Ss),
sublist([6,_,_,_,_,_,_,6,_,_,_,_,_,_,6], Ss),
sublist([5,_,_,_,_,_,5,_,_,_,_,_,5], Ss),
sublist([4,_,_,_,_,4,_,_,_,_,4], Ss),
sublist([3,_,_,_,3,_,_,_,3], Ss),
sublist([2,_,_,2,_,_,2], Ss),
sublist([1,_,1,_,1], Ss).

%question(Ss). 

%an w write de xem day du danh sach, an h de tro giup