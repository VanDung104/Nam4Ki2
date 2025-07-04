%%[swi('demo/likes')].
%%[swi('demo/loves')].
%%[swi('doc/packages/examples/cpp/likes')].
%%[swi('D:/Prolog/examples/loves')].
%%['D:/Prolog/examples/loves'].
%%[swi('D:\\Prolog\\examples\\loves')].

%%['D:/Prolog/examples/loves'].

likes(mary,john).
likes(mary,potplants).
likes(mary,jane).
likes(mary,paul).
likes(mary,'Heartbreak High').
likes(john,mary).
likes(fidothedog,mary).
likes(mary,sunbathing).
likes(bugs,mary).
likes(john,'The X files').
likes(paul,mary).
likes(paul,sue).

person(mary).
person(john).
person(sue).
person(paul).
person(jane).

happy(X) :-
    person(X),
    likes(Y, X),
    person(Y).


loves(X,Y) :-
    person(X),
    likes(Y, X),
    likes(X, Y),
    person(Y).