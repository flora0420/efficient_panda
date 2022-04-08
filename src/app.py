import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import inspect
from typing import List


# a function to time how long it takes to run a function n times
@st.experimental_memo
def time_this(func_str, *args, n=10):
    # st.experimental_memo cannot hash function.
    func = eval(func_str)
    import time
    start = time.time()
    for _ in range(n):
        func(*args)
    end = time.time()
    return end - start

# a function to read a raw data file from the web into a pandas dataframe 
@st.cache()   
def read_data():
    df = pd.read_csv('https://raw.githubusercontent.com/mlabonne/how-to-data-science/main/data/nslkdd_test.txt')
    return df

# a function to iterate over rows in df to sum two columns using iterrows 
def iterrows_sum(df:pd.DataFrame)->List:
    total = []
    for idx, row in df.iterrows():
        total.append(row['src_bytes'] + row['dst_bytes'])
    return total

# a function to iterate over rows in df to sum two columns using for loop
def for_loop_sum(df:pd.DataFrame)->List:
    total = []
    for idx in range(df.shape[0]):
        total.append(df['src_bytes'].loc[idx] + df['dst_bytes'].loc[idx])
    return total

# a function to iterate over rows in df to sum two clumns using apply
def apply_sum(df:pd.DataFrame)->List:
    return df.apply(lambda row: row['src_bytes'] + row['dst_bytes'], axis=1).to_list()

# a function to iterate over rows in df to sum two columns using itertuples
def itertuples_sum(df:pd.DataFrame)->List:
    total = []
    for row in df.itertuples():
        total.append(row.src_bytes + row.dst_bytes)
    return total

# a function to iterate over rows in df to sum two columns using list comprehension
def list_comprehension_sum(df:pd.DataFrame)->List:
    total = [src + dst for src, dst in zip(df['src_bytes'], df['dst_bytes'])]
    return total

#  a function to iterate over rows in df to sum two columns using pandas vectorization
def pandas_vectorization_sum(df:pd.DataFrame)->List:
    return (df.src_bytes + df.dst_bytes).to_list()

# a function to iterate over rows in df to sum two columns using numpy vectorization
# def numpy_vectorization_sum(df):
#     return np.add(df['src_bytes'], df['dst_bytes']).tolist()
def numpy_vectorization_sum(df:pd.DataFrame)->List:
    return (df['src_bytes'].to_numpy() + df['dst_bytes'].to_numpy()).tolist()

# a function to plot the results using pyplot
def plot_results(results:pd.DataFrame, title:str):
    # create a bar chart from the dataframe df_results use pyplot
    fig = plt.figure(figsize=(6,3))
    ax = fig.add_axes([0,0,1,1])
    ax.bar(results['method'], results['time'])
    ax.set_xticklabels(results['method'], rotation=90)
    ax.set_ylabel('time (s) in log scale')
    ax.set_title(title)
    ax.set_yscale('log')
    return fig

def main():
    st.title("Iterating Rows in a DataFrame")
    st.markdown("### What is the most efficient way to iterate over rows in a dataframe")
    st.write("Credits to [@Maxime Labonne](https://medium.com/@mlabonne) [his medium post](https://medium.com/towards-data-science/efficiently-iterating-over-rows-in-a-pandas-dataframe-7dd5f9992c01).")
    df = read_data()

    st.subheader("Data")
    st.write('''This dataset has **22k rows and 43 columns** 
    with a combinaton of categorial and numerical values.
    Each row describes a connection betwen two computers.''')

    st.subheader("Tasks")
    st.write("Create a new feature: the total number of bytes in the connection.")
    st.write("Sepcifically, we need to sum up `src_bytes` and `dst_bytes`.")
    
    st.subheader("Iteration Method")
    methods = {
        "iterrows": 'iterrows_sum',#'1x',
        "for loop": 'for_loop_sum', #"3x", 
        "apply": 'apply_sum', #"4x", 
        "itertuples": 'itertuples_sum',# "10x",
        "list comprehension": 'list_comprehension_sum',# "200x",
        "pandas vectorization": 'pandas_vectorization_sum',# "1500x", 
        "numpy vectorization": 'numpy_vectorization_sum'# "1900x"
        }
    st.sidebar.subheader("Ways to iterate over rows")
    st.sidebar.selectbox(
        "Select an iteration method", options = methods.keys(),
        key='selected_method')

    st.sidebar.write("---")
    st.sidebar.subheader("For timing the function")
    st.sidebar.text_input(
        "Number of repeats", 10, key='n_repeats')

    st.write('The selected method is:', methods[st.session_state['selected_method']])
    st.code(f'{inspect.getsource(eval(methods[st.session_state["selected_method"]]))}')

    st.subheader(f"Results ({st.session_state['n_repeats']} repeats)")
    # dict to store the results
    results = dict.fromkeys(methods.keys(), 0)

    for key, func_str in methods.items():
        # time the function
        results[key] = time_this(func_str, df, n=int(st.session_state['n_repeats']))
        # display the results
        rslt_str = f"{key}: {results[key]:.2f} seconds"
        if key != 'iterrows':
            st.write(rslt_str, f"; {results['iterrows']/results[key]:.0f} times faster than iterrows")
        else:
            st.write(rslt_str)

    # create result dataframe from dict results
    df_results = pd.DataFrame.from_dict(results, orient='index', columns=['time'])\
        .reset_index().rename({'index':'method'}, axis=1)
    
    with st.expander("See the results in a plot"):
        fig = plot_results(df_results, title='Time to iterate over rows in a dataframe')
        st.pyplot(fig)


    st.subheader("Conclusion")

    st.image('../images/runtime.png')
    st.write("Image credit to: [@Maxime Labonne](https://medium.com/@mlabonne)")

main()