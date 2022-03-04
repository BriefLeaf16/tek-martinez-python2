import pandas
import sqlalchemy



engine = sqlalchemy.create_engine('mysql+pymysql://root:Maria0729123@localhost/our_puppies')
#CSV for dogs
data = pandas.read_csv('dogs.csv', index_col = False, delimiter = ',')
data.to_sql('puppies', engine, schema = 'our_puppies', if_exists= 'append', index = False)

#CSV for owners
data2 = pandas.read_csv('owners.csv', index_col = False, delimiter = ',')
#data2.to_sql('owners', engine, schema = 'our_puppies', if_exists= 'append', index = False)

print(len(data.index))
print(len(data2.index))


print(len(data.columns))
print(len(data2.columns))

print(data.groupbu('color').size())
