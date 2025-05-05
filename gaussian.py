import numpy as np

#def solve_system_of_equations(A,b):
#    try:
#        solution = np.linalg.solve(A, b)
#        return solution
#    except np.linalg.LinAlgError:
#        return "The system of equations has no unique solution."
    
    
 
def gaussian_elimination(A, b):
    n = len(A)
    augmented = np.hstack((A, b)).astype(float)
    for i in range(n):
        pivot_row = i
        max_val = abs(augmented[i][i])
        for k in range(i+1,n):
            if abs(augmented[k][i]) > max_val:
                max_val = abs(augmented[k][i])
                pivot_row = k
        if pivot_row != i:
            augmented[[i, pivot_row]] = augmented[[pivot_row, i]].copy()
        if abs(augmented[i][i]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular.")
        pivot_row = augmented[i][i]
        augmented[i] = augmented[i] / pivot_row
        for j in range(i+1, n):
            factor = augmented[j][i]
            augmented[j] = augmented[j] - factor * augmented[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = augmented[i][-1]
        for j in range(i+1, n):
           x[i] = x[i] - np.sum(augmented[i][j] * x[j])
    return x         
    
A = np.array([[3,-1,-1], [1,1,0],[2,0,-3]])


b = np.array([5,0,2]).reshape(-1, 1)


c = gaussian_elimination(A, b)
print("Solution:", c)


#a = np.array([[1,2,3],[5,4,5],[8,6,7]])
#b_i = np.array([[7],[8],[9]])
#b = np.array([7,8,9]).reshape(-1, 1)
#t = np.column_stack((a,b)).astype(float)
#print(b_i)
#print(b)
#print(t)
