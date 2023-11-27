# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
from llama_index.indices.struct_store import GPTPandasIndex
import os
import re
import json

st.markdown("""
          <style>
          footer {visibility: hidden;}
          </style>""", unsafe_allow_html=True)

with st.sidebar:
        #openai_api_key = st.text_input('Your OpenAI API KEY', type="password")
        os.environ['OPENAI_API_KEY'] = st.text_input('Your OpenAI API KEY', type="password")


pattern = r"\bgraph\b"

st.title("Greenlync Zulu")

file = st.file_uploader("Upload csv file", type=["csv"])

if file:
    df = pd.read_csv(file)
    index = GPTPandasIndex(
        df=df,
    )
    query_engine = index.as_query_engine(
        verbose=True
    )
    text = st.text_input("Enter your query:")

    if text:
        if re.search(pattern, text):
            query = text.replace("create a graph of", "")
            query = query + " in json of only required columns"
            response = query_engine.query(query)
            response = str(response)
            data = json.loads(response)
            graph = pd.DataFrame(data)

            st.markdown("<b>Response:</b>", unsafe_allow_html=True)
            st.bar_chart(graph)
        else:
            response = query_engine.query(text)
            st.markdown("<b>Response:</b>", unsafe_allow_html=True)
            st.text(response)
