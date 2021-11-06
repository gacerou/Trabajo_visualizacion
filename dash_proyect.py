#-------------------------------------------------------------------------------
# Name:        dash_project.py
# Purpose:
#
# Author:      Gustavo ibarra
#              German Acero
#
# Created:     30/10/2021
# Copyright:   (c) ASUS 2021
# Licence:     Apache 2.0
#-------------------------------------------------------------------------------

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
colors = {
    'background': 'blue',
    'text': '#7FDBFF'
}
bdo = pd.read_csv('base_de_suficiencia.csv', sep=';', encoding='latin-1')

Columnas = bdo.columns

TipoC = bdo['Subgrupo'].unique()

TipoC_m = [ 'TUMOR MALIGNO DE LA MAMA',
            'TUMORES MALIGNOS DE LOS ORGANOS DIGESTIVOS',
            'TUMORES MALIGNOS DE LA GLANDULA TIROIDES Y DE OTRAS GLANDULAS ENDOCRINAS',
            'TUMORES MALIGNOS DE SITIOS MAL DEFINIDOS, SECUNDARIOS Y DE SITIOS NO ESPECIFICADOS',
            'TUMORES DE COMPORTAMIENTO INCIERTO O DESCONOCIDO',
            'MELANOMA Y OTROS TUMORES MALIGNOS DE LA PIEL',
            'TUMORES MALIGNOS DE LOS HUESOS Y DE LOS CARTLAGOS ARTICULARES',
            'TUMORES BENIGNOS',
            'TUMORES MALIGNOS DEL OJO, DEL ENCEFALO Y DE OTRAS PARTES DEL SISTEMA NERVIOSO CENTRAL',
            'TUMORES MALIGNOS DEL LABIO DE LA CAVIDAD BUCAL Y DE FARINGE',
            'TUMORES MALIGNOS DEL TEJIDO LINFATICO, DE LOS ORGANOS HEMATOPEYETICOS Y DE TEJIDOS AFINES',
            'TUMORES MALIGNOS DE LOS ORGANOS GENITALES FEMENINOS',
            'TUMORES MALIGNOS DE LOS ORGANOS RESPIRATORIOS E INTRATORACICOS',
            'TUMORES IN SITU',
            'TUMORES MALIGNOS DE LOS TEJIDOS MESOTELIALES Y DE LOS TEJODOS BLANDOS',
            'TUMORES MALIGNOS DE SITIOS MULTIPLES',
            'TUMORES MALIGNOS DE LOS ORGANOS GENITALES MASCULINOS',
            'TUMORES MALIGNOS DE LAS VIAS URINARIAS']

card_content = [

    dbc.CardHeader("Card header"),

    dbc.CardBody([

        html.H5("Card title", className="card-title"),
        html.P(
            "This is some card content that we'll reuse",
            className="card-text",
        )
    ]),
]


card_E1 = [

    dbc.CardHeader("Cantidad de Usuarios por Departamento", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Ubar')
    ]), 
]

card_E2 = [

    dbc.CardHeader("Relación entre el valor total y la edad ", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Uscatter')
    ]), 
]

card_E3 = [

    dbc.CardHeader("Relación entre el valor total y la edad ", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Upie')
    ]), 
]

row_1 = dbc.Row([
    dbc.Col(dbc.Card(card_E1, color="primary"  , outline=True, className = 'Gcard')),
    dbc.Col(dbc.Card(card_E2, color="secondary", outline=True, className = 'Gcard')),
    dbc.Col(dbc.Card(card_E3, color="info"     , outline=True, className = 'Gcard')),
],className="mb-4")

card_E4 = [

    dbc.CardHeader("Relación entre el valor total y la edad ", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Ubox')
    ]), 
]

card_E5 = [

    dbc.CardHeader("Relación entre el valor total y la edad ", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Uscatter_3')
    ]), 
]

card_E6 = [

    dbc.CardHeader("Relación entre el valor total y la edad ", className='H-Card'),
    dbc.CardBody([
        dcc.Graph(id='Uscatter_2')
    ]), 
]

row_2 = dbc.Row([
    dbc.Col(dbc.Card(card_E4, color="primary"  , outline=True, className = 'Gcard')),
    dbc.Col(dbc.Card(card_E5, color="secondary", outline=True, className = 'Gcard')),
    dbc.Col(dbc.Card(card_E6, color="info"     , outline=True, className = 'Gcard')),
],className="mb-4")
#agregado por german

bdo['Per_capita']=(bdo['Valor Procedimiento-Medicamento-Insumo']/bdo['Usuarios'])/1000
pv =pd.pivot_table(bdo,index=['Departamento','Subgrupo'],values=['Per_capita','Número de Atenciones'],
aggfunc={'Per_capita':sum,'Número de Atenciones':sum},fill_value=0)

pv2 =bdo[(bdo.Capítulo == 'C_M_P_D')]
pv2=pv2.groupby(by=['Subgrupo']).sum('Número de Atenciones')
pv2=pv2.rename(columns={'Número de Atenciones':'consulta'})
pv3=pd.merge(pv, pv2,on='Subgrupo')
pv3['serv/consul']=pv3['Número de Atenciones']/pv3['consulta']
pv3['frecuencia']=pv3['Número de Atenciones']/pv3['Usuarios']
pv3 = pv3 .reset_index()

pv0 = pd.DataFrame(bdo[['Subgrupo','Departamento','Per_capita']].groupby(['Subgrupo','Departamento']).count())
pv0 = pv0 .reset_index()
pv0 = pv0[['Departamento', 'Per_capita','Subgrupo']].sort_values('Per_capita', ascending = False)
pv0 =pv0.pivot(index='Departamento',columns='Subgrupo',values='Per_capita')
pv0=pv0[['T_benignos','C_I','Mama','Org_D','Piel']]
am1 = go.Figure(
   data=[go.Bar(x=pv0.index,y=pv0['T_benignos'],name='Tumores beningnos',marker=dict(color="#3498db")),
       go.Bar(x=pv0.index,y=pv0['C_I'],name='tumores de comportamiento incierto',marker=dict(color='#f1c40f')),
       go.Bar(x=pv0.index,y=pv0['Mama'],name='CA_Mama', marker=dict(color="#d633bb"))],
       layout=go.Layout(title='costos per capita por principales caceres' ))

pv02 =pd.pivot_table(bdo,index=['Departamento'],columns=['Ambito del Procedimiento'],values=['Per_capita'],
aggfunc=sum,fill_value=0)
am21=go.Bar(x=pv02.index,y=pv02[('Per_capita','A ')],name='ambulatorio')
am22=go.Bar(x=pv02.index,y=pv02[('Per_capita','H ')],name='hospitalario')
am32=go.Bar(x=pv02.index,y=pv02[('Per_capita','D ')],name='domiciliario')
am42=go.Bar(x=pv02.index,y=pv02[('Per_capita','U ')],name='Urgencia')



pv02 =pd.pivot_table(bdo,index=['Departamento'],columns=['Ambito del Procedimiento'],values=['Per_capita'],
aggfunc=sum,fill_value=0)
am21=go.Bar(x=pv02.index,y=pv02[('Per_capita','A ')],name='ambulatorio')
am22=go.Bar(x=pv02.index,y=pv02[('Per_capita','H ')],name='hospitalario')
am32=go.Bar(x=pv02.index,y=pv02[('Per_capita','D ')],name='domiciliario')
am42=go.Bar(x=pv02.index,y=pv02[('Per_capita','U ')],name='Urgencia')

pv01 = pd.DataFrame(pv3[['Subgrupo','serv/consul']].groupby(['Subgrupo']).sum())
pv01 = pv01 .reset_index()
am2 = go.Figure(
   data=[go.Bar(x=pv01['Subgrupo'],y=pv01['serv/consul'],name='servicios por consulta',marker=dict(color="#3498db"))
       ],
       layout=go.Layout(title='Servicios por consulta' ))
#hasta aqui agregado german
app.layout = html.Div([

    html.H1('Análisis del comportamiento del consumo asociado a cáncer en Colombia'),

    html.Div(className='BrSpace'),

    html.P('La presente investigación se enfocará en el análisis del comportamiento de los costos de salud en Colombia asociados a diagnósticos de cáncer mediante la utilización de SISPRO en el segmento de información relacionada con la base de suficiencia de UPC, lo cual brindara información al tomador de decisión, con la cual poder evaluar las diferentes políticas públicas a implementar para la gestión y cumplimiento de metas en la atención de Cáncer en el país o bien sea desde un organismo regional como lo es un departamento teniendo en cuenta la asignación de recursos garantice la atención en salud de los pacientes.'),

    html.Div(className='BrSpace'),

    dbc.Tabs([

        # información Base de datos
        dbc.Tab([
            html.Div([

                html.Div([

                    html.H2('Objetivos'),

                    html.H3('Objetivos Generales'),

                    html.P('Analizar los comportamientos de los servicios en salud asociados a Cáncer en Colombia y predecir características o comportamiento según consumo.'),

                    html.H3('Objetivos Específicos'),

                    html.Ul([
                        html.Li('Establecer el comportamiento de consumos y su cambio según características de edad y sexo.'),
                        html.Li('Determinar las diferencias de prestación de servicios que pueden existir por región.'),
                        html.Li('Identificar si los servicios contratados por modalidad de contratación por cápita son más económicos que los que no están bajo esta modalidad.'),
                        html.Li('Generar un modelo que explique el costo de los servicios según tipo de cáncer'),
                        html.Li('Establecer las categorías de servicio que mayor peso tienen en el costo como en el número de servicios prestados.'),
                    ]),
                ], className='Obj_container'),

                html.Div([

                    html.H2('Base de Datos'),

                    html.Ul([
                        html.Li('Cantidad de Registros: 729100'),
                        html.Li('Cantidad de Variables: 11'),
                        html.Li('Variables Cualitativas: 7'),
                        html.Li('Variables Cuantitativas: 4'),
                        html.Li('Archivo: base_de_suficiencia.csv'),
                        html.Li('Fuente: SISPRO')
                    ]),
                ], className='Obj_container'),

            ],className='text_container'),

            html.H2('Variables'),

            html.H3('Variables Cualitativas'),

            html.Ul([
                html.Li('Clasificación de los códigos de servicios de acuerdo a 28 capítulos'),
                html.Li('Clasificación del cáncer por subgrupo de diagnóstico CIE10 en'),
                html.Li('Departamento: Da el departamento donde se realizó el servicio'),
                html.Li('Tipo de servicio: Determina se el servicio fue en el régimen contributivo o subsidiado'),
                html.Li('Forma de reconocimiento: Es una variable cualitativa donde se clasifica los distintos tipos de contrato contemplados para la prestación del servicio'),
                html.Li('Ámbito del procedimiento: Muestra en que espacio se realizó el servicio'),
                html.Li('Sexo: Identifica el género de la persona'),
            ]),

            html.H3('Variables Cuantitativas'),
            
            html.Ul([
                html.Li('EDAD: Número de años del usuario'),
                html.Li('Numero de servicios: Numero de servicios realizados'),
                html.Li('Usuarios: Número de personas que recibieron el servicio'),
                html.Li('Valor procedimiento: Costo global de utilización del servicio '),
                html.Li('Valor procedimiento promedio: valor promedio del servicio unitario'),
            ]),
            
        ], label = 'Introducción', className = 'TabsP-Tab' ),

        # Descripción Estadística
        dbc.Tab([

            html.H2('Tipo de Cáncer'),

            dcc.Dropdown(
                id='Ucancer',
                value = 'cancer',
                options = [{'label': cancer, 'value' : str(cancer)}
                    for cancer in TipoC_m]
            , className = 'Dp-Cancer'),

            row_1,

            row_2,

        ], label = 'Descripción Estadística', className = 'TabsP-Tab'),

        # KPI's
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.P('Se establecieron tres KPi como principales metricas para el entendimiento del consumo de cáncer en colombia,los Kpi seleccionados fueron:'),
                html.Li('Costo per capita'),
                html.Li('Peso de hospitalización en el costo'),
                html.Li('servicios por consulta'),html.H3('indicadores')
            ]),
        html.Legend("Costo percapita"),dcc.Graph(id = 'bar',figure=am1),
        html.Li('Con este indicador podemos ver cual es el departamento con el mayor costo por usuario de cáncer'),
        html.Legend("Proporcion hospitaliza"),dcc.Graph(id = 'bar2',figure={'data': [am21,am22,am32,am42],'layout':go.Layout(title='ambitos')}),
        html.Li('Dentro de este indicador se puede establecer cual es el departamento con el mayor numero decosto asociado a hospitalización'),
        html.Legend("Servicios por consulta"),dcc.Graph(id = 'bar3',figure=am2),
        html.Li('Mediante este indicador se puede establecer cual es el cancer con mayor numero de servicios generados')], label = 'Indicadores', className = 'TabsP-Tab'),

        # Modelo Estadístico
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('Se desarrrollo un modelo de regresión multiple con el fin de poder explicar el costo de cancer y poder predecir el impacto',style={'color':'white', 'fontSize':'18px'}),
                html.Li('El modelo agrupa las variables que mejor explican el costo teniendo en cuanta que sean significativas dentro del modelo',style={'color':'white', 'fontSize':'18px'}),
                html.Li('El modelo desarrollado tiene un R^2 del 44% de explicación', style={'color':'white', 'fontSize':'18px'}),
            ]),html.Ul([ html.Br(),html.Li('Ecuacion:Costo_total=96,540+Capita*-671,900+Regimen*383,400+Consulta*-522,400+Micelaneo* 3,377,000+M_Nuclear_radio*2,496,000+R_centro*597,800+R_pacifico*408,600+R_oriente*729,900+Edad*3,364+Usuarios*120,900+Valor*1.21+Ambito*-406,400+Sexo*-144,400 ', style={'color':'white', 'fontSize':'18px'})])
              ,html.Br(),html.Label('A continuación coloque las variables necesarias segu caracteristicas de población para determinnar el costo total'),html.Div([
            "Capita:                      ",
            dcc.Input(id='Capita', value=0, type='number',min=0, max=1),
            html.Br(),
            "Regimen:                     ",dcc.Input(id='Regimen', value=0, type='number',min=0, max=1),
            html.Br(),
            "Consulta:                     ",dcc.Input(id='Consulta', value=0, type='number',min=0, max=1),
            html.Br(),
            "Micelaneo:                    ",dcc.Input(id='Micelaneo', value=0, type='number',min=0, max=1),
            html.Br(),
            "Medicina nuclear:             ",dcc.Input(id='M_nuclear', value=0, type='number',min=0, max=1),
            html.Br(),
            "Region centro:                ",dcc.Input(id='R_centro', value=0, type='number',min=0, max=1),
            html.Br(),
            "Region pacifico:              ",dcc.Input(id='R_pacifico', value=0, type='number',min=0, max=1),
            html.Br(),
            "Region oriente:               ",dcc.Input(id='R_oriente', value=0, type='number',min=0, max=1),
            html.Br(),
            "Edad:                         ",dcc.Input(id='Edad', value=0, type='number',min=0, max=1),
            html.Br(),
            "Numero de usuarios atendidos: ",dcc.Input(id='Usuarios', value=0, type='number'),
            html.Br(),
            "Valor medio del servicio:     ",dcc.Input(id='Valor', value=0, type='number'),
            html.Br(),
            "Ambito:                       ",dcc.Input(id='Ambito', value=0, type='number',min=0, max=1),
            html.Br(),
            "Sexo:                         ",dcc.Input(id='Sexo', value=0, type='number',min=0, max=1),
            ]),html.Br(),
           html.Br(),
    "Valor en pesos calculado : ",html.Div(id='my-output')], 
        label = 'Modelo Estadístico', className = 'TabsP-Tab'),

    html.Div(className='BrSpace')]),

    #Footer
    html.Div([

        dbc.Card([
            
            dbc.CardBody([
                html.H4('Integrantes: ', className= 'h3-inte'),

                html.Ul([
                    html.Li('Gustavo A. Ibarra P.', className='Li-inte'),
                    html.Li('German Acero Acero', className='Li-inte'),
                    html.Li('Nelso Julio Villamil', className='Li-inte'),
                ], className = 'Ul-inte'),
            ])
        ]), 
    ])
], className ='divBorder')

@app.callback(Output('Upie', 'figure'),
                Input('Ucancer', 'value'))


def plot_variable_pie(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]

    data = bdo[bdo['Subgrupo'] == c]
    data = data[['Sexo','Usuarios']].groupby(['Sexo']).sum()

    fig = px.pie(values=data['Usuarios'], names=data.index)
    return fig

@app.callback(Output('Ubar','figure'),
                Input('Ucancer', 'value'))

def barplot_variable(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]
    
    bd2 = pd.DataFrame(bdo[['Subgrupo','Departamento','Sexo','Usuarios']].groupby(['Subgrupo','Departamento','Sexo']).sum())
    bd2 = bd2.reset_index()
    bd2 = bd2[bd2['Subgrupo'] == c]
    bd2 = bd2[['Departamento', 'Usuarios','Sexo']].sort_values('Usuarios', ascending = False)
    bd2 = bd2[0:10]

    fig = px.bar(bd2, x='Departamento', y='Usuarios', color='Sexo')
    fig.update_traces( textposition='outside')
    fig.update_layout( uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

@app.callback(Output('Uscatter','figure'),
                Input('Ucancer', 'value'))

def scatter_variable(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]
    
    bd2 = bdo[bdo['Subgrupo'] == c]
    bd2 = bdo[['Usuarios','Sexo','Edad','Número de Atenciones']].groupby(['Sexo','Edad']).sum()
    bd2 = bd2.reset_index()
    
    fig = px.scatter(bd2, x="Número de Atenciones", y="Usuarios", color="Sexo",
                        size='Edad')
    return fig

@app.callback(Output('Uscatter_2','figure'),
                Input('Ucancer', 'value'))

def scatter_2_variable(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]
    
    bd2 = bdo[['Subgrupo','Sexo','Edad','Número de Atenciones','Tipo Servicio','Ambito del Procedimiento']]
    bd2 = bd2.reset_index()
    bd2 = bd2[bd2['Subgrupo'] == c]
    
    fig = px.scatter(bd2, x="Número de Atenciones", y="Edad", facet_row="Sexo", facet_col="Tipo Servicio", color="Ambito del Procedimiento")

    return fig

@app.callback(Output('Uscatter_3','figure'),
                Input('Ucancer', 'value'))

def scatter_3_variable(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]
    
    bd2 = bdo[bdo['Subgrupo'] == c]
    bd2 = bd2[['Sexo','Edad','Número de Atenciones']]
    bd2 = bd2.reset_index()
       
    fig = px.scatter(bd2, x="Número de Atenciones", y="Edad", color="Sexo", marginal_y="box",
           marginal_x="box", template="simple_white")

    return fig

@app.callback(Output('Ubox','figure'),
                Input('Ucancer', 'value'))

def boxplot_variable(cancer):
    j = TipoC_m.index(cancer)
    c = TipoC[j]
    
    data = bdo[bdo['Subgrupo'] == c]
    data = data[['Sexo','Ambito del Procedimiento','Usuarios']]
    data = data.reset_index()
    
    fig = px.box(data, x="Ambito del Procedimiento", y="Usuarios", color="Sexo")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default

    return fig

@app.callback(Output('my-output','children'),
Input(component_id='Capita',component_property='value'),
Input(component_id='Regimen',component_property='value'),
Input(component_id='Consulta',component_property='value'),
Input(component_id='Micelaneo',component_property='value'),
Input(component_id='M_nuclear',component_property='value'),
Input(component_id='R_centro',component_property='value'),
Input(component_id='R_pacifico',component_property='value'),
Input(component_id='R_oriente',component_property='value'),
Input(component_id='Edad',component_property='value'),
Input(component_id='Usuarios',component_property='value'),
Input(component_id='Valor',component_property='value'),
Input(component_id='Ambito',component_property='value'),
Input(component_id='Sexo',component_property='value'))
def modelo(Capita,Regimen,Consulta,Micelaneo,M_nuclear,R_centro,R_pacifico,R_oriente,Edad,Usuarios,Valor,Ambito,Sexo):
    return 96540+(Capita*-671900)+(Regimen*383400)+(Consulta*-522400)+(Micelaneo* 3377000)+(M_nuclear*2496000)+(R_centro*597800)+(R_pacifico*408600)+(R_oriente*729900)+(Edad*3364)+(Usuarios*120900)+(Valor*1.21)+(Ambito*-406400)+(Sexo*-144400) 

if __name__ == '__main__':
    app.run_server(debug=True)