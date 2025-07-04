
%%['D:/Prolog/examples/nqueen'].


del(Item,[Item|List],List). 
del(Item,[First|List],[First|List1]) :-
 del(Item,List,List1).

permutation([],[]). 
permutation([Head|Tail],PermList) :-
 permutation(Tail,PermTail),
 del(Head,PermList,PermTail).

noattack(_,[],_). 
noattack(Y,[Y1|Ylist],Xdist) :-
 Y1-Y=\=Xdist,
 Y-Y1=\=Xdist,
 Dist1 is Xdist + 1,
 noattack(Y,Ylist,Dist1).
  
safe([]).
safe([Queen|Others]) :-
 safe(Others),
 noattack(Queen,Others,1).
 
solution(Queens) :-
 permutation([1,2,3,4,5,6,7,8], Queens),
 safe(Queens).
 