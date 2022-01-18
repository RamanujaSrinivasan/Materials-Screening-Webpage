# from __future__ import division  https://github.com/obedsims/batt_dispatch
import streamlit as st
import pandas as pd
import os
# from st_aggrid import AgGrid
st.set_page_config(layout="wide")

# Title
st.title("Web tool for the screening of materials for energy applications")
st.markdown('A Web App by Murugan.P and Ramanuja Srinivasan.S, CSIR-CECRI, Karaikudi, India')
st.markdown("")
st.write("Hello, Researchers!")
st.markdown("This is a web tool developed for the screening of materials for energy applications. By using the toggle bars, compounds with desired properties can be screened!")
with st.expander("Data Information"):
    st.markdown("The results are imported from Materials Project (https://materialsproject.org/) via interactive python tool Pymatgen (https://pymatgen.org/).")
st.markdown("")

# Sidebar Content
st.sidebar.markdown("**Screening Parameters**")
# Band_Gap1 = st.sidebar.number_input('Band Gap (eV)', value=0.0, min_value=0.0, max_value=10.0, step=0.1)
Band_Gap = st.sidebar.slider('Band Gap (eV)', min_value=0.0, max_value=10.0, step=0.1, value=(0.0,0.5), format=None, key=None, help=None, on_change=None, args=None, kwargs=None)
Gravimetric_Capacity = st.sidebar.slider('Gravimetric Capacity (mAh/g)', value=(0,40), min_value=0, max_value=9000, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)
Energy_above_Hull = st.sidebar.slider('Energy above Hull', value= (0.0,0.90) , min_value=0.0, max_value=3.5, step=0.1, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)
F_Block = st.sidebar.selectbox("F-Block (Lanthanides and Actinides)",("Include","Exclude"))
Unfit_elements = st.sidebar.selectbox("Unfit elements [Cd,Hg,As,Be,Pb,Rh,Ru,Au,Pt,Ir,Cr,Ag]",("Include","Exclude"))
experimental_icsd_id = st.sidebar.selectbox("Experimental compounds (False = Experimentally achieved)",("Include","Exclude"))


# filename = st.text_input('Enter a file path:')
# df = pd.read_excel(filename)
#
SAVE_PATH = os.path.join(os.getcwd(), 'Downloads')
# filepath = st.text_input('Enter a file path:')
# filenameq = st.text_input('Enter file name:')
# filename = filepath + "\\" + filenameq
# uploaded_file = st.file_uploader(filename) #
uploaded_file = st.file_uploader("Chosse a file") #
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header = 0, sheet_name="Initial")
    st.write(df)
# df.to_excel(os.path.join(SAVE_PATH, filenameq+"Ver1"))
if F_Block == "Exclude":
  df2 = df[df['F-Block']]
  df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
if Unfit_elements == "Exclude":
  df2 = df[df['Unfit elements']]
  df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
if experimental_icsd_id == "Include":
  df2 = df[df['Experimental ICSD ID']]
  df3 = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
  df = pd.concat([df, df3, df3]).drop_duplicates(keep=False)

df2 = df[df['Noble-Gas']]
df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
df2 = df[df['Gaseous Compounds']]
df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)

df = df[df['Band gap'].between(Band_Gap[0], Band_Gap[1])]
df = df[df['Gravimetric Capacity'].between(Gravimetric_Capacity[0], Gravimetric_Capacity[1])]
param_tech = df[df['Energy above Hull'].between(Energy_above_Hull[0], Energy_above_Hull[1])]

st.write("Number of compounds screened : ", len(param_tech))
with st.expander("Screening info"):
  st.markdown("The results are already screened for the exclusion of Gaseous compounds.")
is_check = st.checkbox("Display Data")
if is_check:
  st.table(param_tech)
# st.write(df)

# file_path = st.text_input("Paste your data path here : ")
# os.chdir(file_path)
#
# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)
#
# filename = file_selector()
# st.write('You selected `%s`' % filename)

# df = pd.read_excel(str(file_path)+str(filename), sheet_name='Initial')

# df = pd.read_excel(r"C:\Users\Ramanujam\PycharmProjects\Pymatgenexecute\Code without weight filter\fluorideNew.xlsx", sheet_name='Initial')







import plotly.express as px
hmap_params = st.multiselect("Select parameters to include on heatmap", options=list(df.columns), default=[p for p in df.columns if "fg" in p])
hmap_fig = px.imshow(df[hmap_params].corr())
st.write(hmap_fig)


hist_x = st.selectbox("Histogram variable", options=df.columns, index=df.columns.get_loc("Band gap"))
hist_bins = st.slider(label="Histogram bins", min_value=None, max_value=None, value=None, step=None)
hist_fig = px.histogram(df, x=hist_x, nbins=hist_bins)# streamlit run data_explorerst_app.py   ## Terminal
title=("Histogram of Compounds") #, template = "plotly_white"
st.write(hist_fig)

# import pandas as pd
# import plotly.express as px
# import streamlit as st
# st.write("Hello, Researchers!")
# st.write("This is a web tool developed for the screening of materials for energy applications. By using the toggle bars, compounds with desired properties can be screened!")
# df = pd.read_excel(r"C:\Users\Ramanujam\PycharmProjects\Pymatgenexecute\Code without weight filter\fluorideNew.xlsx", sheet_name='Initial')
# hist_x = st.selectbox("Histogram variable", options=df.columns, index=df.columns.get_loc("Band gap"))
# hist_bins = st.slider(label="Histogram bins", min_value=None, max_value=None, value=None, step=None)
# hist_fig = px.histogram(df, x=hist_x, nbins=hist_bins)# streamlit run data_explorerst_app.py   ## Terminal
# title=("Histogram of ") #, template = "plotly_white"
# st.write(hist_fig)
# hmap_params = st.multiselect("Select parameters to include on heatmap", options=list(df.columns), default=[p for p in df.columns if "fg" in p])
# hmap_fig = px.imshow(df[hmap_params].corr())
# st.write(hmap_fig)

# if dispatch_method == "Maximise Self Consumption":
#     E1 = dispatch_max_sc(pv, demand, param_tech, return_series=False)
#     plot_dispatch(pv, demand, E1, week=week)
#     print_analysis(pv, demand, param_tech, E1)
# if dispatch_method == "Peak Shave":
#     E1 = dispatch_max_sc_grid_pf(pv, demand, param_tech, return_series=False)
#     plot_dispatch(pv, demand, E1, week=week)
#     print_analysis(pv, demand, param_tech, E1)
# if dispatch_method == "Minimise Costs (LP Optimisation)":
#     E1 = dispatch_min_costs(pv, demand, param_tech, return_series=False)
#     plot_min_cost_dispatch(pv, demand, E1, week=week)
#     print_min_cost_analysis(pv, demand, param_tech, E1)

# dispatch_method = st.sidebar.selectbox("Select Application",
#                                        ["Battery", "Peak Shave", "Minimise Costs (LP Optimisation)"])
# week = st.sidebar.slider(label="Select the week of data you want to view:",
#                          min_value=1, max_value=52, value=20, format='Week %d')


# mp_id = df["MP-ID"]
# Pretty_formula = df["Pretty Formula"]
# Composition = df["Composition"]
# F_Block = df["F-Block"]
# Noble_gas = df["Noble-Gas"]
# Unfit_elements = df["Unfit elements"]
# Gaseous_compounds = df["Gaseous Compounds"]
# ICSD_ids = df["ICSD_IDS"]
# experimental_icsd_id = df["Experimental ICSD ID"]
# space_group = df["Space Group Symbol"]
# crystal_system = df["Crystal System"]

# param_tech = {'MP-ID':mp_id,
#               'Pretty Formula':Pretty_formula,
#               'Band Gap': Band_Gap,  # kWh
#               'Gravimetric Capacity': Gravimetric_Capacity,  # dimensionless
#               'Energy above Hull': Energy_above_Hull,
#               'F-Block':F_Block,
#               'Noble-Gas':Noble_gas,
#               'Unfit elements':Unfit_elements,
#               'Gaseous Compounds':Gaseous_compounds,
#               'ICSD_IDS':ICSD_ids,
#               'Experimental ICSD ID':experimental_icsd_id,
#               'Space Group Symbol':space_group,
#               'Crystal System':crystal_system
#               }

# param_tech1 = pd.DataFrame(param_tech)

# dffinaltest = df[Band_Gap & Gravimetric_Capacity & Energy_above_Hull]
# dffinaltest = df.loc[Band_Gap & Gravimetric_Capacity & Energy_above_Hull]

# param_tech = {'Band Gap': Band_Gap,  # kWh
#               'Gravimetric Capacity': Gravimetric_Capacity,  # dimensionless
#               'Energy above Hull': Energy_above_Hull}


# import pandas as pd
# df = pd.read_excel(r"C:\Users\Ramanujam\PycharmProjects\Pymatgenexecute\Code without weight filter\fluorideNew.xlsx", sheet_name='Initial')
# from pandasgui import show
# gui = show(df)

# df = df[Band_Gap]
# param_tech = df[df["Band Gap"].Band_Gap]

# import urllib
# weburl = urllib.request.urlopen('https://github.com/RamanujaSrinivasan/Materials-Screening-Webpage/blob/main/fluorideNew.xlsx')
# # data = weburl.read()
# xd = pd.ExcelFile(weburl)
#
# import pandas as pd
# link =r'https://github.com/RamanujaSrinivasan/Materials-Screening-Webpage/blob/main/fluorideNew.xlsx'
# data = pd.read_excel(link,sheet_name='Initial', engine="openpyxl")
#
# import pandas as pd
# link =r'D:\fluorideNew.csv'
# data = pd.read_csv(link, delimiter=',', header=0)
#
#
# #
# # from RPA.core.robocorp. import xcel.Files import Files
# # from RPA.HTTP import HTTP
#
# excel_lib = Files()
# http_lib = HTTP()
#
# excel_file_url= "https://github.com/robocorp/example-web-store-order-processor/raw/main/devdata/Data.xlsx"
#
#
# def download_the_excel_file(url):
#     http_lib.download(url, overwrite=True)
#
# def open_the_file_as_table():
#     excel_lib.open_workbook("Data.xlsx")
#     table = excel_lib.read_worksheet_as_table(header=True)
#     excel_lib.close_workbook()
#     return table
#
# def loop_over_table(table):
#     for row in table:
#         print(row)
#
# # Define a main() function that calls the other functions in order:
# def main():
#     download_the_excel_file(excel_file_url)
#     table = open_the_file_as_table()
#     loop_over_table(table)
#
# # Call the main() function, checking that we are running as a stand-alone script:
# if __name__ == "__main__":
#     main()



# from numpy import loadtxt
# from urllib.request import urlopen
# url = 'https://github.com/npradaschnor/Pima-Indians-Diabetes-Dataset/blob/master/diabetes.csv'
# raw_data = urlopen(url)
# dataset = loadtxt(raw_data)
#
# import pandas as pd
# data=pd.read_excel('https://github.com/npradaschnor/Pima-Indians-Diabetes-Dataset/blob/master/diabetes.csv')
