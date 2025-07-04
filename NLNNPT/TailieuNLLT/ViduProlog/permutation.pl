%%[swi('demo/likes')].
%%[swi('demo/loves')].
%%[swi('doc/packages/examples/cpp/likes')].
%%[swi('D:/Prolog/examples/loves')].
%%['D:/Prolog/examples/loves'].
%%[swi('D:\\Prolog\\examples\\loves')].

%%['D:/Prolog/examples/permutation'].

del(Item,[Item|List],List).
del(Item,[First|List],[First|List1]) :-
 del(Item,List,List1).

permute([],[]). 
permute([Head|Tail],PermList) :-
 permute(Tail,PermTail),
 del(Head,PermList,PermTail).
 
sequence(_,[]).
sequence(N,[H|T]) :-
    N1 is N - 1,
    sequence(N,H),
    sequence(N1,T).

