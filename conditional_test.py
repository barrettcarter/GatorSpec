def cond(param=True):
    if param == False:
        print('I am done!')
        return
    print('2+2=4')
    print('Now I am done.')
    
cond(param=False)
cond()