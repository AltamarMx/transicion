#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import plotly.express as px
import colormaps as cmaps
import seaborn as sns


# In[28]:


def filtra_maxyear(co2):
    return co2[co2.Year == co2.Year.max()]


# In[29]:


f = "../data/co-emissions-per-capita.csv"
co2_percapita = pd.read_csv(f)
co2_percapita = filtra_maxyear(co2_percapita)

f = "../data/co2-intensity.csv"
co2_intensity = pd.read_csv(f)
co2_intensity = filtra_maxyear(co2_intensity)

f = "../data/annual-co2-emissions-per-country.csv"
co2_percountry = pd.read_csv(f)
co2_percountry = filtra_maxyear(co2_percountry)


# Combinar los tres DataFrames por 'Entity', 'Code', y 'Year'
co2_combined = co2_percapita[['Entity', 'Code', 'Year', 'Annual CO₂ emissions (per capita)']].merge(
    co2_intensity[['Entity', 'Code', 'Year', 'Annual CO₂ emissions per GDP (kg per international-$)']], 
    on=['Entity', 'Code', 'Year'], how='outer'
).merge(
    co2_percountry[['Entity', 'Code', 'Year', 'Annual CO₂ emissions']], 
    on=['Entity', 'Code', 'Year'], how='outer'
)

co2_combined


# In[30]:


co2_percapita.columns, co2_percountry.columns, co2_intensity.columns


# In[36]:


# Crear el mapa coroplético
fig = px.choropleth(filtra_maxyear(co2_percapita), 
                    locations='Code', 
                    color='Annual CO₂ emissions (per capita)', 
                    hover_name='Entity', 
                    color_continuous_scale=px.colors.sequential.Jet,
                    labels={'Annual CO₂ emissions (per capita)': 'Emisiones de CO₂ per cápita (toneladas)'},
                    title='Emisiones de CO₂ per cápita por país en 2022'
                   )

fig.update_layout(
    width=1000,  # Ancho de la figura
    height=600,  # Alto de la figura
)

# Mostrar la gráfica
fig.show()


# In[43]:


# Filtrar y cargar los datos
df = co2_percapita

# Discretizar los datos en 10 intervalos
df['CO₂ discretized'] = pd.cut(df['Annual CO₂ emissions (per capita)'], bins=10, labels=False)

# Obtener una paleta de colores discreta de seaborn con 10 colores
colors = sns.color_palette("rocket", n_colors=10).as_hex()

# Crear el mapa coroplético
fig = px.choropleth(
    df, 
    locations='Code', 
    color='CO₂ discretized',  # Usar los datos discretizados
    hover_name='Entity', 
    color_continuous_scale=colors,  # Aplicar la paleta de colores discretos
    labels={'CO₂ discretized': 'CO₂<br>[ton]'},
)

# Ajustar la posición y orientación de la barra de color
fig.update_layout(
    width=1000,  # Ancho de la figura
    height=600,  # Alto de la figura
    coloraxis_colorbar=dict(
        orientation='h',  # Orientar la barra de color en horizontal
        x=0.5,  # Centrar la barra de color en el eje X
        y=-0.15,  # Colocar la barra de color por debajo del mapa
    ),
    margin={"r":0,"t":50,"l":0,"b":50},  # Ajustar márgenes para dar espacio a la barra de color
    geo=dict(
        showframe=False,  # Quitar el borde del mapa
        showcoastlines=False,  # Quitar las líneas de costa
        showland=False,  # Quitar la representación de tierra
    )
)

# Mostrar la gráfica
fig.show()

