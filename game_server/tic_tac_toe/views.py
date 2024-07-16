from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from rest_framework import status

import pymongo

# Create your views here.

client = pymongo.MongoClient("mongodb+srv://stks01201:c2y4G7KOkEXNFBOe@jokepool.lygjfjw.mongodb.net/")
player_collection = client["main2"]["players"]
game_collection = client["main2"]["games"]

def place_move(game, position, player):

    '''
    place the move
    return the next player
    '''

    if game['board'][position] != '-':
        return False

    mark = "X" 

    if game['player2'] == player:
        mark = 'O'
    
    if len(game['order']) >= 6:
        move_to_delete = int(game['order'][-1])
        game['board'] = game['board'][0:move_to_delete] + '-' + game['board'][move_to_delete+1:]
    
    game['order'] = str(position) + game['order'][0:5]

    game['board'] = game['board'][0:position] + mark + game['board'][position+1:]

    game_collection.find_one_and_update({'_id':game['_id']}, {"$set" : game})

    # return game.player1 if mark == "O" else game.player2
    return True


def check_winner(game):

    winner = "-"

    if game['board'][0] == game['board'][4] == game['board'][8] or \
        game['board'][3] == game['board'][4] == game['board'][5] or \
        game['board'][6] == game['board'][4] == game['board'][2] or \
        game['board'][1] == game['board'][4] == game['board'][7]:
        winner = game['board'][4]
    elif game['board'][0] == game['board'][1] == game['board'][2] or \
        game['board'][0] == game['board'][3] == game['board'][6]:
        winner = game['board'][0]
    elif game['board'][8] == game['board'][5] == game['board'][2] or \
        game['board'][8] == game['board'][7] == game['board'][6]:
        winner = game['board'][8]
    
    return winner

def index(request):
    return render(request, "index.html")

@api_view(['POST'])
def create_player(request):
    result = player_collection.insert_one({})
    player_id = result.inserted_id
    return JsonResponse({"player_id" : player_id})

@api_view(['POST'])
def find_opponent(request):
    input = JSONParser().parse(request)
    player_id = input["id"]
    player_obj = player_collection.find_one({"_id" : player_id})
    if not player_obj:
        return JsonResponse({"status" : 500 , "message" : "Invalid player id"})

    if game_collection.find_one({"player2" : ""}, {"$set": {"player2": player_id}}):
        return JsonResponse({"status" : 200 , "message" : "Player found"})

    game_collection.insert_one({
        "player1" : player_id,
        "player2" : "",
        "board" : "---------",
        "order" : ""
    })
    return JsonResponse({"status" : 200 , "message" : "Searching for player"})

    

@api_view(['POST'])
def join_game(request):
    input = JSONParser().parse(request)
    player_id = input["id"]

    return JsonResponse({"message" : "Unable to handle request"})

@api_view(['POST'])
def leave_game(request):
    input = JSONParser().parse(request)
    player_id = input["id"]

    return JsonResponse({"message" : "Unable to handle request"})

@api_view(['POST'])
def make_move(request):
    input = JSONParser().parse(request)
    player_id = input["id"]
    position = input["position"]

    return JsonResponse({"message" : "Unable to handle request"})

