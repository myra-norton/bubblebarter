import random

for i in range(10):
    funcs = ['logout login', 'logout login2', 'post', 'edit', 'accept', 'propose']
    funclist = 'login'
    for j in range(random.randint(1, 15)):
        funclist += ' ' + random.choice(funcs)
    print(funclist)