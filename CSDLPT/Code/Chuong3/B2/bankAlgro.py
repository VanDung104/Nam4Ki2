import numpy as np

class BankersAlgorithm:
    def __init__(self, available, max_demand, allocation):
        self.available = np.array(available)  
        self.max_demand = np.array(max_demand)  
        self.allocation = np.array(allocation)  
        self.need = self.max_demand - self.allocation  

    def is_safe(self):
        """Kiểm tra trạng thái an toàn của hệ thống"""
        work = np.copy(self.available)
        finish = np.zeros(len(self.need), dtype=bool)
        safe_sequence = []

        while len(safe_sequence) < len(self.need):
            allocated = False
            for i in range(len(self.need)):
                if not finish[i] and np.all(self.need[i] <= work):
                    work += self.allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated = True
                    break
            if not allocated:
                return False, []
        
        return True, safe_sequence

# Ví dụ hệ thống có 3 tài nguyên và 3 tiến trình
# available = [3, 3, 2]  # Tài nguyên có sẵn
# max_demand = [[7, 5, 3], [3, 2, 2], [9, 0, 2]]  # Nhu cầu tối đa
# allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2]]  # Tài nguyên đã cấp phát
available = [3, 3, 2]
max_demand = [[5, 5, 3], [2, 2, 2], [4, 2, 2]]
allocation = [[1, 1, 1], [1, 0, 1], [2, 1, 1]]


bankers = BankersAlgorithm(available, max_demand, allocation)
safe, sequence = bankers.is_safe()

if safe:
    print(f"Hệ thống an toàn! Trình tự thực hiện: {sequence}")
else:
    print("Deadlock sắp xảy ra! Không thể cấp phát tài nguyên!")
