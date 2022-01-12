# from __future__ import division  https://github.com/obedsims/batt_dispatch
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
st.set_page_config(layout="wide")
df = pd.read_excel(r"C:\Users\Ramanujam\PycharmProjects\Pymatgenexecute\Code without weight filter\fluorideNew.xlsx", sheet_name='Initial')


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
experimental_icsd_id = st.sidebar.selectbox("Experimental ICSD ID (Exclude = Experimentally achieved)",("Include","Exclude"))


if F_Block == "Exclude":
    df2 = df[df['F-Block']]
    df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
if Unfit_elements == "Exclude":
    df2 = df[df['Unfit elements']]
    df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)
if experimental_icsd_id == "Exclude":
    df2 = df[df['Experimental ICSD ID']]
    df = pd.concat([df, df2, df2]).drop_duplicates(keep=False)

df = df[df['Band gap'].between(Band_Gap[0],Band_Gap[1])]
df = df[df['Gravimetric Capacity'].between(Gravimetric_Capacity[0],Gravimetric_Capacity[1])]
param_tech = df[df['Energy above Hull'].between(Energy_above_Hull[0],Energy_above_Hull[1])]

st.write("Number of compounds screened : ",len(param_tech))
is_check = st.checkbox("Display Data")
if is_check:
    st.table(param_tech)

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


# df = df[Band_Gap]
# param_tech = df[df["Band Gap"].Band_Gap]
