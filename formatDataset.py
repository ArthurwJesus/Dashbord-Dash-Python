#
import pandas as pd


#Funções de leitura e iniciação dos dados puros do csv
def team():

    team = pd.read_csv('./datasets/teams_fifa23.csv')

    return team


def players():

    players = pd.read_csv('./datasets/players_fifa23.csv')

    return players


#Tratando os dados para escolher os 10 melhores baseando-se no Overall
def bestTeams():
    team()
    bestTeams = team().query("`Overall` >= 80")

    return bestTeams


def bestPlayers():
    players()

    bestPlayers = players().query("`Overall` >= 85")

    return bestPlayers


#Escolhendo o jogador

def selectPlayer(input_value):

    select_player = input_value

    player = players().query('Name == @select_player')  # filtrando o dataframe inicial para apenas o nome do jogador

    return player