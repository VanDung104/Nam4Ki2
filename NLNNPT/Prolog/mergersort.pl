% Merge Sort trong Prolog

% Trường hợp cơ sở: danh sách rỗng hoặc có một phần tử thì giữ nguyên.
merge_sort([], []).
merge_sort([X], [X]).

% Nếu danh sách có nhiều hơn một phần tử, chia nhỏ rồi sắp xếp.
merge_sort(List, Sorted) :-
    divide(List, Left, Right),         % Chia danh sách thành hai nửa
    merge_sort(Left, SortedLeft),      % Sắp xếp nửa bên trái
    merge_sort(Right, SortedRight),    % Sắp xếp nửa bên phải
    merge(SortedLeft, SortedRight, Sorted). % Trộn hai danh sách đã sắp xếp

% Hàm chia danh sách thành hai phần
divide([], [], []).
divide([X], [X], []).
divide([X,Y|Rest], [X|Left], [Y|Right]) :-
    divide(Rest, Left, Right).

% Hàm trộn hai danh sách đã sắp xế
merge([], R, R).
merge(L, [], L).
merge([X|L], [Y|R], [X|M]) :- X =< Y, merge(L, [Y|R], M).
merge([X|L], [Y|R], [Y|M]) :- X > Y, merge([X|L], R, M).
