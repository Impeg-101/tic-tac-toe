import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import views

import pymongo

class GameConsumer(WebsocketConsumer):

    client = pymongo.MongoClient("mongodb+srv://stks01201:c2y4G7KOkEXNFBOe@jokepool.lygjfjw.mongodb.net/")
    player_collection = client["main2"]["players"]
    game_collection = client["main2"]["games"]

    def connect(self):
        print("connection open")
        self.accept()


    def disconnect(self, close_code):
        print("connection closed")
        player = self.player_collection.find_one_and_delete({"channel_name" : self.channel_name})
        if not player:
            return
        game = self.game_collection.find_one_and_delete({"$or": [{"player1" : player['name']},{ "player2" : player['name']}]})
        if not game:
            return
        async_to_sync(self.channel_layer.group_send)(
            str(game['_id']),
            {
                # message telling player 1 to make a move and player 2 to wait
                'type' : 'game_cancel',
                'player left' : player['name']
            }
        )
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        name = text_data_json['name']

        player_obj = self.player_collection.find_one_and_update({"name" : name}, {"$set": {'channel_name' : self.channel_name}})
        # here we get the obj first and check if the channel_name exist, if it does then the name is already in session
        if not player_obj:
            result = self.player_collection.insert_one({'name' : name, 'channel_name' : self.channel_name})
            player_obj = self.player_collection.find_one({"_id": result.inserted_id})

        if text_data_json['type'] == 'find-game':

            gameObj = self.game_collection.find_one_and_update({"player2" : None}, {"$set": {"player2": player_obj['name']}})

            if gameObj:
                async_to_sync(self.channel_layer.group_add)(
                    str(gameObj['_id']),
                    self.channel_name
                )

                # self.send(text_data=json.dumps({
                #     'type' : "found"
                # }))

                async_to_sync(self.channel_layer.group_send)(
                    str(gameObj['_id']),
                    {
                        # message telling player 1 to make a move and player 2 to wait
                        'type' : 'playing',
                        'player to make move' : gameObj['player1'],
                        'board' : gameObj['board']
                    }
                )

                return

            game_id = self.game_collection.insert_one({
                "player1" : player_obj['name'],
                "player2" : None,
                "board" : "---------",
                "order" : "",
            }).inserted_id

            async_to_sync(self.channel_layer.group_add)(
                str(game_id),
                self.channel_name
            )

            self.send(text_data=json.dumps({
                'type' : "finding"
            }))

        elif text_data_json['type'] == 'exit-game':
            pass
        elif text_data_json['type'] == 'make-move':
            position = text_data_json['position']

            gameObj = self.game_collection.find_one({"$or": [{"player1" : player_obj['name']},{ "player2" : player_obj['name']}]})

            print(gameObj)

            #check if the player id match the player's turn
            # last_mark = gameObj['order'][-1] if len(gameObj['order']) > 0 else ''
            # if (last_mark == 'X' or '' and player_obj['name'] == gameObj['player2']['name']) or (last_mark == 'O' and player_obj['name'] == gameObj['player1']['name']):
            #     return self.send(text_data=json.dumps({
            #         'type' : 'move not accepted'
            #     }))



            views.place_move(gameObj, position, player_obj['name'])

            async_to_sync(self.channel_layer.group_send)(
                str(gameObj['_id']),
                {
                    # message telling player 1 to make a move and player 2 to wait
                    'type' : 'playing',
                    'player to make move' : gameObj['player1'] if player_obj['name'] == gameObj['player2'] else gameObj['player2'],
                    'board' : gameObj['board']
                }
            )

            # check if won
            winner = views.check_winner(gameObj)
            print("winner is ", winner)
            if winner != '-':
                async_to_sync(self.channel_layer.group_send)(
                    str(gameObj['_id']),
                    {    
                        'type' : 'game_over',
                        'winner' : gameObj['player1'] if winner == 'X' else gameObj['player2']
                    })
            print("here")


        elif text_data_json['type'] == '':
            pass

    def playing(self, text_data):
        self.send(text_data=json.dumps(text_data))

    def update_board(self, text_data):
        self.send(text_data=json.dumps(text_data))
    
    def game_over(self, text_data):
        self.send(text_data=json.dumps(text_data))

    def game_cancel(self, text_data):
        self.send(text_data=json.dumps(text_data))