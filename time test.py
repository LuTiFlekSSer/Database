import time
from matplotlib import pyplot
import random
import db

times = [10 ** x for x in range(7)]
add_st = []
add_test = []
edit_test = []
create_test = []
del_test = []
for x in times:
    db.create_db('1')
    t = time.time()
    for _ in range(x):
        db.add_student('q w e')
    add_st.append(time.time() - t)

    t = time.time()
    for _ in range(x):
        db.add_test(str(random.random))
    add_test.append(time.time() - t)

    t = time.time()
    for _ in range(x):
        db.edit_test(0, str(random.random))
    edit_test.append(time.time() - t)

    t = time.time()
    db.create_testing_table()
    create_test.append(time.time() - t)

    t = time.time()
    for _ in range(x):
        db.del_test(0)
    del_test.append(time.time() - t)
    db.del_db('1')

pyplot.plot(times, add_st, label='add st')
pyplot.plot(times, add_test, label='add test')
pyplot.plot(times, create_test, label='create testing table')
pyplot.plot(times, edit_test, label='edit test')
pyplot.plot(times, del_test, label='del test')
pyplot.legend()
pyplot.grid()
pyplot.show()