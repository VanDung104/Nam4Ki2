
function hamLoc(condition) {
    return function(numbers) {
        return numbers.filter(condition);
    };
}


const soChan = (num) => num % 2 === 0;   // Số chẵn
const soLe = (num) => num % 2 !== 0;    // Số lẻ
const lonHon5 = (num) => num > 5;   // Lớn hơn 5


const locChan = hamLoc(soChan);
const locLe = hamLoc(soLe);
const locLonHon5 = hamLoc(lonHon5);


const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

console.log(locChan(numbers));        
console.log(locLe(numbers));         
console.log(locLonHon5(numbers));
