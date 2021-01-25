import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


st.header("Data Visualizer Web App")
st.markdown("##### created by Sahil Kirpekar")
st.write("\n")

file = st.file_uploader('Upload CSV File Here')
st.write("\n")



def xy_input(a,b):
	x = st.sidebar.selectbox("Choose X axis feature",a)
	y = st.sidebar.selectbox("Choose Y axis feature",b)
	return x, y


def kind_of_plot(df):

	df_col_names = list(df.columns)
	df_col_int = list(df.select_dtypes(include=["uint8","float64","int64"]).columns)
	df_col_str = list(df.select_dtypes(include="object").columns)

	kplot = st.sidebar.selectbox("What kind of plot?",["Scatterplot","Jointplot","Barplot","Histplot","Violinplot","Boxplot","Heatmap","Swarmplot","Stripplot"])


	if kplot == "Scatterplot":
		x, y = xy_input(df_col_int, df_col_int)
		color = st.sidebar.selectbox("Choose Color",["red","blue","cyan","orange","yellow"])
		marker = st.sidebar.selectbox("Choose Marker",["o","+","*"])
		fig = plt.figure(figsize=(10,8))
		plt.scatter(x=df[x],y=df[y],c=color,marker=marker)
		plt.xlabel(x)
		plt.ylabel(y)
		st.pyplot(fig)

	elif kplot == "Barplot":
		x = st.sidebar.selectbox("Choose data feature",df_col_int)
		h = st.sidebar.selectbox("Height w.r.t. which feature",df_col_int)
		w = st.sidebar.slider("Width",0.1,1.0,0.8)
		axis = st.sidebar.selectbox("Axis",["X","Y"])
		fig = plt.figure(figsize=(10,8))
		if axis == "X":
			plt.bar(x=df[x],width=w,height=df[h])
		if axis == "Y":
			plt.barh(y=df[x],width=w,height=df[h])
		plt.xlabel(x)
		plt.ylabel(h)
		st.pyplot(fig)
	elif kplot == "Jointplot":
		x, y = xy_input(df_col_int, df_col_int)
		kind = st.sidebar.selectbox("What kind of jointplot?",["scatter","kde","reg","hex"])
		df_str = df_col_str
		df_str.append(None)
		hue = st.sidebar.selectbox("Hue",df_str)
		fig = plt.figure()
		sns.jointplot(x=x,y=y,data=df,hue=hue,kind=kind)
		st.pyplot()
	elif kplot == "Histplot":
		y = st.sidebar.selectbox("Choose Y axis feature",df_col_int)
		bins = st.sidebar.number_input('Bins',5,100)
		fig = plt.figure(figsize=(10,8))
		plt.hist(df[y], bins=bins,linewidth=0.4, edgecolor="black")
		plt.xlabel("Frequency")
		plt.ylabel(y)
		st.pyplot(fig)
	elif kplot == "Violinplot":
		x, y = xy_input(df_col_str, df_col_int)
		fig = plt.figure(figsize=(10,8))
		sns.violinplot(x=x,y=y,data=df,hue=x,dodge=True)
		plt.xlabel(x)
		plt.ylabel(y)
		st.pyplot(fig)
	elif kplot == "Boxplot":
		x, y = xy_input(df_col_str, df_col_int)
		fig = plt.figure(figsize=(10,8))
		sns.boxplot(x=x,y=y,data=df,hue=x,dodge=True)
		plt.xlabel(x)
		plt.ylabel(y)
		st.pyplot(fig)
	elif kplot == "Heatmap":
		show_all = st.sidebar.selectbox("Show all features?",["Yes","No"])
		if show_all == "Yes":
			fig=plt.figure()
			sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
			st.pyplot(fig)
		elif show_all == "No":
			feat = st.sidebar.multiselect("Select features",df_col_int)
			if len(feat) >=2:
				fig = plt.figure(figsize=(20,20))
				fig=plt.figure()
				sns.heatmap(df[list(feat)].corr(),annot=True,cmap="coolwarm",vmin=0,)
				st.pyplot(fig)
			else:
				st.sidebar.info("Select 2 or more label features to get a heatmap")
	elif kplot == "Swarmplot":
		x, y = xy_input(df_col_str, df_col_int)
		fig = plt.figure(figsize=(10,8))
		sns.swarmplot(x=x,y=y,data=df,dodge=True)
		plt.xlabel(x)
		plt.ylabel(y)
		st.pyplot(fig)
	elif kplot == "Stripplot":
		x, y = xy_input(df_col_str, df_col_int)
		fig = plt.figure(figsize=(10,8))
		sns.stripplot(x=x,y=y,data=df,edgecolor="black",linewidth=0.2,jitter=True)
		plt.xlabel(x)
		plt.ylabel(y)
		st.pyplot(fig)




if file:
	df = pd.read_csv(file)

	st.write("\nData\n",df.head())

	st.set_option('deprecation.showPyplotGlobalUse', False)
	kind_of_plot(df)