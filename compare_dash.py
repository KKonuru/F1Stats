import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#imports for the fastf1 api
import fastf1
import datetime
import requests

from bs4 import BeautifulSoup

fastf1.Cache.enable_cache('cache')

#This method uses the ergast API to generate a list of the event names for the year passed 
def get_raceEvents(year):
    EventFullNames = []
    url = "https://ergast.com/api/f1/"+str(year)+".json"
    response = requests.get(url)
    data = response.json()
    races = data["MRData"]["RaceTable"]["Races"]
    for race in races:
        EventFullNames.append(race["raceName"])
    return EventFullNames

def getDriverNames(year,round,session):
    url = "http://ergast.com/api/f1/"+str(year)+"/"+str(round)+"/qualifying.json"
    if session=="race":
        url="https://ergast.com/api/f1/"+str(year)+"/"+str(round)+"/results.json"
    response = requests.get(url)
    data = response.json()
    drivers = list()
    if session =="race":
        var="Results"
    else:
        var="QualifyingResults"
    
    races = data["MRData"]["RaceTable"]["Races"][0][var]
    for row in races:
        driverDict = row["Driver"]
        drivers.append(driverDict["givenName"]+" "+driverDict["familyName"])
    return drivers 

def getDriverCode(year,name):
    url = "https://ergast.com/api/f1/"+str(year)+"/drivers.json"
    response = requests.get(url)
    data = response.json()
    drivers = data["MRData"]["DriverTable"]["Drivers"]
    for driver in drivers:
        if driver["givenName"]+" "+driver["familyName"]==name:
            return driver["code"]

def getRoundNumber(year,name):
   url = "https://ergast.com/api/f1/"+str(year)+".json"    
   response = requests.get(url)
   data = response.json()
   races = data["MRData"]["RaceTable"]["Races"]
   for race in races:
      if race["raceName"]==name:
         return race["round"]

def create_dash_app(flask_app):
    dash_app = dash.Dash(server=flask_app,name="Dashboard",url_base_pathname="/compare/",assets_folder='assets',external_stylesheets=[dbc.themes.BOOTSTRAP])


    dash_app.layout = html.Div(children = [html.Link(rel='stylesheet',href='/assets/colors.css'),
                                                            html.H1('F1 Data Analytics',className = 'accent text-black-center'),
                                                            dcc.Dropdown(id='site-dropdown',options=[{'label':i,'value':i} for i in range(2019,datetime.date.today().year +1)],value=2023,placeholder="Select a race year",searchable=True),
                                                            #Dynamic dropdown where the value selected in the first dropdown is passed to the second dropdown
                                                            dcc.Dropdown(id='race-dropdown',value="Bahrain Grand Prix",placeholder="Select a Formula 1 Race",searchable=True),
                                                            #html.Div(id="output"),
                                                            dcc.Dropdown(id="session",options=[{'label':'Qualifying','value':'Qualifying'},{'label':'Race','value':'Race'}],value="Race",placeholder="Select a Formula 1 session"),
                                                            dcc.Dropdown(id='driver-dropdown',value="Fernando Alonso",placeholder="Select a driver",searchable=True),
                                                            dcc.Dropdown(id='driver-dropdown2',value="Fernando Alonso",placeholder="Select a driver",searchable=True),
                                                            #html.Div(id="output2"),
                                                            html.Div([ ],id="plot1"),
                                                            

    ])

    @dash_app.callback(dash.dependencies.Output('race-dropdown','options'),
                [dash.dependencies.Input('site-dropdown','value')])
    def update_dropdown(year):
        return [{'label':i,'value':i} for i in get_raceEvents(year)]

    @dash_app.callback(dash.dependencies.Output('driver-dropdown','options'),
                [dash.dependencies.Input('site-dropdown','value'),
                dash.dependencies.Input('race-dropdown','value'),
                dash.dependencies.Input('session','value')])
    def update_driver_dropdown(year,race,session):
        roundNumber  = getRoundNumber(year,race)
        drivers = getDriverNames(year,roundNumber,session)
        return [{'label':driver,'value':driver} for driver in drivers]

    @dash_app.callback(dash.dependencies.Output('driver-dropdown2','options'),
                [dash.dependencies.Input('site-dropdown','value'),
                dash.dependencies.Input('race-dropdown','value'),
                dash.dependencies.Input('session','value')])
    def update_driver_dropdown(year,race,session):
        roundNumber  = getRoundNumber(year,race)
        drivers = getDriverNames(year,roundNumber,session)
        return [{'label':driver,'value':driver} for driver in drivers]


    #This callback is used to update the graph based on the selection of the driver,race,session, and year
    @dash_app.callback(dash.dependencies.Output("plot1","children"),
                    [dash.dependencies.Input('site-dropdown','value'),
                    dash.dependencies.Input('race-dropdown','value'),
                    dash.dependencies.Input('session','value'),
                    dash.dependencies.Input('driver-dropdown','value'),
                    dash.dependencies.Input('driver-dropdown2','value')],
                    [dash.dependencies.State('plot1','children')])
    def get_driver_lapGraph(year,race,session,driver,driver2,child):
        sessionObj = fastf1.get_session(year,race,session)
        sessionObj.load()
        fast_lec = sessionObj.laps.pick_driver(getDriverCode(year,driver))
        lec_car_data= fast_lec.get_car_data()
        t = lec_car_data['Time']
        vCar = lec_car_data['Speed']


        fig = make_subplots(rows=1,cols=1)
        fig.add_trace(go.Scatter(x=t,y=vCar),row=1,col=1)

        fig.update_layout(height=600,width=800,title_text="Speed graph bwoah")
        #Create a subplot using plotly and the time data (t) and speed data (vCar)

        return dcc.Graph(figure=fig)
    return dash_app




