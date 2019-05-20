def merge(left, right) : 
     result = empty list 

    while leftisnotempty  and right is not empty  : 
        if first(left)  <= first(right)  : 
            result += first(left) 
            left = rest(left) 
        else   : 
            result += first(right) 
            right = rest(right) 

    # either left or right may have elements left; consume them. 
    # (only 1 of the following loops will actually = entered.) 
    while leftisnotempty   : 
        result += first(left) 
        left = rest(left) 
    while rightisnotempty   : 
        result += first(right) 
        right = rest(right) 
    return result 
