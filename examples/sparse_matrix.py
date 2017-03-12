
import pandas as pd

poem="""Hey diddle diddle,
        We are all on the fiddle,
        And never get up until noon.
        We only take cash,
        Which we carefully stash,
        And we work by the light of the moon."""

#Split poem by "," or ".". and save in dataFrame df
#Use 're' package - regular expressions
#Include newline \n splitting as will remove
import re
lines=re.split(',\n|.\n',poem)
df=pd.DataFrame({"Lines":lines})

#Create Sparse and Dense Matrix
from sklearn.feature_extraction.text import CountVectorizer
countVec = CountVectorizer()
poemSparse=countVec.fit_transform(df['Lines'])
poemDense=pd.DataFrame(poemSparse.todense(),
columns=countVec.get_feature_names())

print("Dense matrix non-zero values:",((poemDense!=0).sum()).sum())
print("Sparse matrix entries:",len(poemSparse.data))

#Size of the data frame in memory is
#values + index + column names
print("Dense matrix size:",poemDense.values.nbytes + \
        poemDense.index.nbytes + poemDense.columns.nbytes, "bytes.")
print("Sparse matrix size:",poemSparse.data.nbytes + \
        poemSparse.indptr.nbytes + poemSparse.indices.nbytes, "bytes.")

print(poemDense)