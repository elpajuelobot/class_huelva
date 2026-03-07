import pandas as pd

df = pd.read_csv('titanic.csv')

df.drop(['PassengerId', "Name", "Ticket", "Cabin"], axis=1, inplace=True)

supervivientes = df.groupby('Sex')['Survived'].mean()

print(f"supervivientes hombres: {round((supervivientes['male'] * 100), 2)}")
print(f"supervivientes mujeres: {round((supervivientes['female'] * 100), 2)}")

print("\n\n\n")

table_survived = (df.pivot_table(
    index='Survived', columns='Pclass',
    values='Age', aggfunc='mean')
)

print(table_survived)

print("\n\n\n")

puerto_supervivientes = df.groupby('Survived')['Embarked'].value_counts()

personas_S_total = puerto_supervivientes[1]['S'] + puerto_supervivientes[0]['S']
personas_C_total = puerto_supervivientes[1]['C'] + puerto_supervivientes[0]['C']
personas_Q_total = puerto_supervivientes[1]['Q'] + puerto_supervivientes[0]['Q']

print(f"personas que han salido del puerto S: {personas_S_total}.\n")
print(f"De las cuales murieron {puerto_supervivientes[0]['S']}\n Y sobrevivieron {puerto_supervivientes[1]['S']}\n\n\n\n")

print(f"personas que han salido del puerto C: {personas_C_total}.\n")
print(f"De las cuales murieron {puerto_supervivientes[0]['C']}\n Y sobrevivieron {puerto_supervivientes[1]['C']}\n\n\n\n")

print(f"personas que han salido del puerto Q: {personas_Q_total}.\n")
print(f"De las cuales murieron {puerto_supervivientes[0]['Q']}\n Y sobrevivieron {puerto_supervivientes[1]['Q']}\n\n\n\n")
