import pandas
try:
    print(pandas.fubar)
    response = pandas.__fubar__
except Exception as e:
    response = str(e)
print(response)


