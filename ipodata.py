import pandas as pd 

address ='http://www.jpx.co.jp/listing/stocks/new/00-archives-02.html'
year = 2015

df = pd.read_html(address)[0]

even = [x for x in range(len(df)) if x % 2 == 0]
odd = [x for x in range(len(df)) if x % 2 == 1]

df1 = df[df.index.isin(even)]
df2 = df[df.index.isin(odd)]
one = [x for x in range(len(df1))]
two = [x for x in range(len(df2))]
df1.index = one
df2.index = two

df1.columns = ['date', 'name', 'code','del','del1','kari','kobo','lot','del2','del3','del4','del5','del6','del7']
df2.columns = ['market','del','del1','price','uri','del2','del3','del4','del5','del6','del7','del8','del9','del10']

df3 = df1[['date','name','code','kari','kobo','lot']]
df4 = df2[['market','price','uri']]

#上場日と上場承認日で分ける
date = {}

for i in df3.index:
	df3.loc[i,'date'] = df3.loc[i,'date'].replace('）','')
	ipodate = df3.loc[i,'date'].split('（')
	date[i] = ipodate

d = pd.DataFrame(date).T 
d.columns =['上場日','上場承認日']

#仮条件の分割
limit = {}

for i in df3.index:
	zyoken = df3.loc[i,'kari'].split('～')
	if df3.loc[i,'kari'] =='-':
		zyoken = ['0','0']
	limit[i] = zyoken

l= pd.DataFrame(limit).T 
l.columns = ['仮条件下限','仮条件上限']

df5 = pd.concat([d,df3[['name','code','kobo','lot']],l], axis=1)

uridashi = {}

ud = df4['uri'].copy()

for i in range(len(ud)):
	ud[i] = ud[i].replace(')','')
	ud[i] = ud[i].replace('OA','')
	urid = ud[i].split('(')
	if ud[i] =='-':
		urid = ['0','0']
	if len(urid) ==1:
		urid.append('0')
	uridashi[i] = urid 

u = pd.DataFrame(uridashi).T
u.columns = ['売り出し(千株)', 'オーバーアロットメント(千株)']

df6 = pd.concat([df4[['market','price']],u],axis=1)

df7 = pd.concat([df5,df6],axis=1)
df7.columns = ['上場日','上場承認日','会社名','コード','公募株数(千株)','売買単位','仮条件下限','仮条件上限','市場','公募価格','売り出し(千株)','オーバーアロットメント(千株)']

df7.to_csv('ipo_{}.csv'.format(year))