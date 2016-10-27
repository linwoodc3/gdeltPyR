
# Cleaning Pipeline

Our goal is to take the CAMEO data from parusanalytics.com and make it "tidy" and ready for data analytics pipelines.  We will use Python `pandas` to clean the data in a few lines of code.  First, let's look at the raw output of the file from pandas.  We will go from "dirty" data to clean data.  Or, specifically we will go from this:
http://eventdata.parusanalytics.com/cameo.dir/CAMEO.SCALE.txt

to these:
* https://github.com/linwoodc3/gdeltPyR/blob/master/utils/schema_csvs/cameoCodeTable.tsv
* https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/utils/schema_csvs/cameoCodes.json

Looking at the data, we'll use a `":"` as the separator.  

Here it is with a standard `pandas` load.


```python
####################
# load pandas
####################

import pandas as pd

# read the file in
pd.read_csv('http://eventdata.parusanalytics.com/cameo.dir/CAMEO.SCALE.txt',sep=':')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>## CAMEO SCALE</th>
      <th>VERSION 0.5B1 [07.03.21]</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>## Philip Schrodt, schrodt@ku.edu</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01</td>
      <td>[0.0] MAKE PUBLIC STATEMENT</td>
    </tr>
    <tr>
      <th>2</th>
      <td>010</td>
      <td>[0.0] Make statement, not specified below</td>
    </tr>
    <tr>
      <th>3</th>
      <td>011</td>
      <td>[-0.1] Decline comment</td>
    </tr>
    <tr>
      <th>4</th>
      <td>012</td>
      <td>[-0.4] Make pessimistic comment</td>
    </tr>
    <tr>
      <th>5</th>
      <td>013</td>
      <td>[0.4] Make optimistic comment</td>
    </tr>
    <tr>
      <th>6</th>
      <td>014</td>
      <td>[0.0] Consider policy option</td>
    </tr>
    <tr>
      <th>7</th>
      <td>015</td>
      <td>[0.0] Acknowledge or claim responsibility</td>
    </tr>
    <tr>
      <th>8</th>
      <td>016</td>
      <td>[3.4] Make empathetic comment</td>
    </tr>
    <tr>
      <th>9</th>
      <td>017</td>
      <td>[0.0] Engage in symbolic act</td>
    </tr>
    <tr>
      <th>10</th>
      <td>018</td>
      <td>[3.4] Express accord</td>
    </tr>
    <tr>
      <th>11</th>
      <td>02</td>
      <td>[3.0] APPEAL</td>
    </tr>
    <tr>
      <th>12</th>
      <td>020</td>
      <td>[3.0] Appeal, not specified below</td>
    </tr>
    <tr>
      <th>13</th>
      <td>021</td>
      <td>[3.4] Appeal for cooperation, not specified below</td>
    </tr>
    <tr>
      <th>14</th>
      <td>0211</td>
      <td>[3.4] Appeal for diplomatic cooperation</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0212</td>
      <td>[3.4] Appeal for material cooperation</td>
    </tr>
    <tr>
      <th>16</th>
      <td>022</td>
      <td>[3.4] Appeal for policy support</td>
    </tr>
    <tr>
      <th>17</th>
      <td>023</td>
      <td>[3.4] Appeal for aid, not specified below</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0231</td>
      <td>[3.4] Appeal for economic aid</td>
    </tr>
    <tr>
      <th>19</th>
      <td>0232</td>
      <td>[3.4] Appeal for military aid</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0233</td>
      <td>[3.4] Appeal for humanitarian aid</td>
    </tr>
    <tr>
      <th>21</th>
      <td>0234</td>
      <td>[3.4] Appeal for military protection or peacek...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>024</td>
      <td>[-0.3] Appeal for political reform, not specif...</td>
    </tr>
    <tr>
      <th>23</th>
      <td>0241</td>
      <td>[-0.3] Appeal for change in leadership</td>
    </tr>
    <tr>
      <th>24</th>
      <td>0242</td>
      <td>[-0.3] Appeal for policy change</td>
    </tr>
    <tr>
      <th>25</th>
      <td>0243</td>
      <td>[-0.3] Appeal for rights</td>
    </tr>
    <tr>
      <th>26</th>
      <td>0244</td>
      <td>[-0.3] Appeal for change in institutions, regime</td>
    </tr>
    <tr>
      <th>27</th>
      <td>025</td>
      <td>[-0.3] Appeal to yield</td>
    </tr>
    <tr>
      <th>28</th>
      <td>026</td>
      <td>[4.0] Appeal to others to meet or negotiate</td>
    </tr>
    <tr>
      <th>29</th>
      <td>027</td>
      <td>[4.0] Appeal to others to settle dispute</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>247</th>
      <td>18</td>
      <td>[-9.0] ASSAULT</td>
    </tr>
    <tr>
      <th>248</th>
      <td>180</td>
      <td>[-9.0] Use unconventional violence, not specif...</td>
    </tr>
    <tr>
      <th>249</th>
      <td>181</td>
      <td>[-9.0] Abduct, hijack, or take hostage</td>
    </tr>
    <tr>
      <th>250</th>
      <td>182</td>
      <td>[-9.5] Physically assault, not specified below</td>
    </tr>
    <tr>
      <th>251</th>
      <td>1821</td>
      <td>[-9.0] Sexually assault</td>
    </tr>
    <tr>
      <th>252</th>
      <td>1822</td>
      <td>[-9.0] Torture</td>
    </tr>
    <tr>
      <th>253</th>
      <td>1823</td>
      <td>[-10.0] Kill by physical assault</td>
    </tr>
    <tr>
      <th>254</th>
      <td>183</td>
      <td>[-10.0] Conduct suicide, car, or other non-mil...</td>
    </tr>
    <tr>
      <th>255</th>
      <td>1831</td>
      <td>[-10.0] Carry out suicide bombing</td>
    </tr>
    <tr>
      <th>256</th>
      <td>1832</td>
      <td>[-10.0] Carry out car bombing</td>
    </tr>
    <tr>
      <th>257</th>
      <td>1833</td>
      <td>[-10.0] Carry out roadside bombing</td>
    </tr>
    <tr>
      <th>258</th>
      <td>184</td>
      <td>[-8.0] Use as human shield</td>
    </tr>
    <tr>
      <th>259</th>
      <td>185</td>
      <td>[-8.0] Attempt to assassinate</td>
    </tr>
    <tr>
      <th>260</th>
      <td>186</td>
      <td>[-10.0] Assassinate</td>
    </tr>
    <tr>
      <th>261</th>
      <td>19</td>
      <td>[-10.0] FIGHT</td>
    </tr>
    <tr>
      <th>262</th>
      <td>190</td>
      <td>[-10.0] Use conventional military force, not s...</td>
    </tr>
    <tr>
      <th>263</th>
      <td>191</td>
      <td>[-9.5] Impose blockade, restrict movement</td>
    </tr>
    <tr>
      <th>264</th>
      <td>192</td>
      <td>[-9.5] Occupy territory</td>
    </tr>
    <tr>
      <th>265</th>
      <td>193</td>
      <td>[-10.0] Fight with small arms and light weapons</td>
    </tr>
    <tr>
      <th>266</th>
      <td>194</td>
      <td>[-10.0] Fight with artillery and tanks</td>
    </tr>
    <tr>
      <th>267</th>
      <td>195</td>
      <td>[-10.0] Employ aerial weapons</td>
    </tr>
    <tr>
      <th>268</th>
      <td>196</td>
      <td>[-9.5] Violate ceasefire</td>
    </tr>
    <tr>
      <th>269</th>
      <td>20</td>
      <td>[-10.0] ENGAGE IN UNCONVENTIONAL MASS  VIOLENCE</td>
    </tr>
    <tr>
      <th>270</th>
      <td>200</td>
      <td>[-10.0] Engage in unconventional mass violence...</td>
    </tr>
    <tr>
      <th>271</th>
      <td>201</td>
      <td>[-9.5] Engage in mass expulsion</td>
    </tr>
    <tr>
      <th>272</th>
      <td>202</td>
      <td>[-10.0] Engage in mass killings</td>
    </tr>
    <tr>
      <th>273</th>
      <td>203</td>
      <td>[-10.0] Engage in ethnic cleansing</td>
    </tr>
    <tr>
      <th>274</th>
      <td>204</td>
      <td>[-10.0] Use weapons of mass destruction, not s...</td>
    </tr>
    <tr>
      <th>275</th>
      <td>2041</td>
      <td>[-10.0] Use chemical, biological, or radiologi...</td>
    </tr>
    <tr>
      <th>276</th>
      <td>2042</td>
      <td>[-10.0] Detonate nuclear weapons</td>
    </tr>
  </tbody>
</table>
<p>277 rows × 2 columns</p>
</div>



For the remainder of this post, we will only show "snippets" of the dataframe.  `pandas` calls this, the "head" of the dataframe.  Our `head` calls below will only show the first few rows of our resulting dataframe, but understand that the operations we are performing are applied to the ENTIRE dataframe/dataset.  The times you see below include computation time on the full dataset.  

## Synopsis of Data and Cleaning Tasks

The data is relatively clean but you see a few problems:

*  columns headrs are improperly formatted and not informative
    *  column 1 has `#` characters
    *  second column's title has no helpful information on the data in the column
* First row can be dropped
* Second column's data contains two observations; the description of the CAMEO code and the corresponding Goldstein Scale number.  We'll need to split it out

We'll handle all of these data cleaning tasks with Pandas.  We can handle the first problem withour read in function.  In the code block below, we set the separator to `":"`, set the header row equal to `None`, define our own column headers as "Description" and "cameoCode", and skip the first two (2) rows of data since they are unnecessary.  


```python
########################################################
# Read file from 
# parusanalytics.com
#########################################################

'''I read in the file, skip the first two rows, create my own header column names'''
scale = pd.read_csv('http://eventdata.parusanalytics.com/cameo.dir/CAMEO.SCALE.txt',
                    sep=':',
                    header=None,
                    dtype={'cameoCode':'str'},
                    names=['cameoCode','Description'],
                   skiprows=2)


```

Let's preview the output of our data.


```python
scale.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cameoCode</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01</td>
      <td>[0.0] MAKE PUBLIC STATEMENT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>010</td>
      <td>[0.0] Make statement, not specified below</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011</td>
      <td>[-0.1] Decline comment</td>
    </tr>
    <tr>
      <th>3</th>
      <td>012</td>
      <td>[-0.4] Make pessimistic comment</td>
    </tr>
    <tr>
      <th>4</th>
      <td>013</td>
      <td>[0.4] Make optimistic comment</td>
    </tr>
  </tbody>
</table>
</div>



# Cleaning Pipeline

### Getting the Goldstein Scale

Now we are ready for the final pieces.  We have to split the `Description` column into two columns.  One column will be the `GoldsteinScale` and the other will be the `Description`. First, we'll use the `pandas` apply function to vectorize a stirng `split` operation on `"]"`, retrieve the first index of the resulting list, and then strip the leading `"["` off the output. We rename this resulting column to **"GoldsteinScale"**. Finally, let's preview the output and print out the time it took for the operation.  


```python
# to keep track of time
import datetime

start = datetime.datetime.now()

# strip the Goldstein data scale to its own column
scale['GoldsteinScale']=scale.Description.apply(
                                            lambda x: pd.Series(x.split(']')[0].strip('[]'
                                             ),
                                            name='GoldsteinScale'))
end = datetime.datetime.now() - start
print('This operation took {0} microsecnds.\n\n'.format(end.microseconds))
scale.head()
```

    This operation took 70414 microsecnds.
    
    





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cameoCode</th>
      <th>Description</th>
      <th>GoldsteinScale</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01</td>
      <td>[0.0] MAKE PUBLIC STATEMENT</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>010</td>
      <td>[0.0] Make statement, not specified below</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011</td>
      <td>[-0.1] Decline comment</td>
      <td>-0.1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>012</td>
      <td>[-0.4] Make pessimistic comment</td>
      <td>-0.4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>013</td>
      <td>[0.4] Make optimistic comment</td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>
</div>



###  Isolating the Description Text

Now we need to isolate the `Description` text.  Using our code above, we will split on the `"]"` character, but this time, we select the second item in the list. We keep the **"Description"** column name but replace the old value with our new value.  Since we have successfully extracted the Goldstein data, we are confident we aren't losing any data on the cutting floor. As always, we preview the output.  


```python

start = datetime.datetime.now()

# strip only description text
scale['Description']=scale.Description.apply(
                                        lambda x: pd.Series(x.split(']')[1],
                                        name='cameoCodeDescription'))
end = datetime.datetime.now() - start
print('This operation took {0} microsecnds.\n\n'.format(end.microseconds))
scale.head()
```

    This operation took 70343 microsecnds.
    
    





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cameoCode</th>
      <th>Description</th>
      <th>GoldsteinScale</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01</td>
      <td>MAKE PUBLIC STATEMENT</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>010</td>
      <td>Make statement, not specified below</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>011</td>
      <td>Decline comment</td>
      <td>-0.1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>012</td>
      <td>Make pessimistic comment</td>
      <td>-0.4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>013</td>
      <td>Make optimistic comment</td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>
</div>



Notice the change in the **Desciption** column.  We removed the brackets and scores and only kept the text.  

###  Cleaning up metadata to write the file

We are done with our cleaning pipeline but we need to clean some things up.  We need to make sure we strip all whitespace from any strings, as trailing whitespace can complicate value lookups.  Additonally, let's write some code to use the cameoCodes as the index to support lookup functionality.  With this implemented, anyone can look up a row using the camoeCode (for python pandas users). More importantly, setting the CAMEO code as the index will use that code as the `key` for the resulting `json` file we create.  We accomplish all of this with three (3) lines of code.  


```python

start = datetime.datetime.now()


# strip whitespace from cameoCode column
scale.cameoCode=scale.cameoCode.apply(lambda x: x.strip())

# set the index to the cameoCode for json lookups
scale.set_index(scale.cameoCode.values,inplace=True)

# rename the index to cameoCode
scale.index.rename('cameoCode',inplace=True)

end = datetime.datetime.now() - start
print('All of these operations took {0} microsecnds total.\n\n'.format(end.microseconds))
scale.head()
```

    All of these operations took 1755 microsecnds total.
    
    





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cameoCode</th>
      <th>Description</th>
      <th>GoldsteinScale</th>
    </tr>
    <tr>
      <th>cameoCode</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>01</th>
      <td>01</td>
      <td>MAKE PUBLIC STATEMENT</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>010</th>
      <td>010</td>
      <td>Make statement, not specified below</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>011</th>
      <td>011</td>
      <td>Decline comment</td>
      <td>-0.1</td>
    </tr>
    <tr>
      <th>012</th>
      <td>012</td>
      <td>Make pessimistic comment</td>
      <td>-0.4</td>
    </tr>
    <tr>
      <th>013</th>
      <td>013</td>
      <td>Make optimistic comment</td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>
</div>



### Final Step: Writing out the cleaned files


The last and most important step, is writing your file out to an open data format that can be used by anyone.  We opt for a `character separated value` (CSV) file.  Specifically, we will use the `tab separated value` flavor of a CSV because our **Description** column contains text with commas. If we used commas as the separator, we would have some problems. For the other format, we chose Javascript Object Notation, or JSON.  Why, it's the language of the web!!!  


```python
# need this to test our load below
import json

#######################
# Write the tsv to disc
#######################

scale.to_csv('/Users/linwood/projects/gdeltPyR/utils/schema_csvs/cameoCodeTable.tsv',
             sep='\t',index=False)


#######################
# test that the csv file
#######################
if len(pd.read_csv('./cameoCodeTable.tsv',
             sep='\t')) > 0:
    print('CSV file is valid')




#######################
# Write the json to disc
#######################

scale.to_json('/Users/linwood/projects/gdeltPyR/utils/schema_csvs/cameoCodes.json')




#######################
# test the json file
#######################

if len(json.load(open('./cameoCodes.json'))) >0:
    print("JSON file is valid")
    
```

    CSV file is valid
    JSON file is valid


### Example of using the JSON for lookups

The JSON file is especially well suited for lookups outside of the Python ecosystem.  Here is an example (in Python) that could be replicated in any other language with their specific JSON handling tools/libraries.  We will look 



```python
# load the file
CAMEOnGoldstein = json.load(open('./cameoCodes.json'))

# look up the description of CAMEO code 193
CAMEOnGoldstein['Description']['193']
```




    ' Fight with small arms and light weapons'



Let's look up the corresponding Goldstein Scale for 193


```python
CAMEOnGoldstein['GoldsteinScale']['193']
```




    '-10.0'



### Conclusion

So, in a few lines of code we have created a machine readable representation of the CAMEO codes for all to use. The CSV/JSON formats are open data formats that can support ANY data science, machine learnign, and data analytics endeavor that needs to translate CAMEO codes to human readable descriptions or Goldstein Scores.  
