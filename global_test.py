global x
x='hi'

def print_x():
    global x
    x = 'hello'
    print(x)
    
print_x()
print(x)