import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, List, ListItem, ListItemText, Typography, Alert, Zoom } from '@mui/material';
import Board from './board';

const Home = () => {
  const [board, setBoard] = useState(["X","","O","","X","","","",""]);
  const [state, setState] = useState("IDLE");
  const [info, setInfo] = useState('');
  const [name, setName] = useState("");
  const [alert, setAlert] = useState("");
  const ws = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket('https://tic-tac-toe-backend-mauve.vercel.app/ws/socket-server/');
    // ws.current = new WebSocket(`ws://${window.location.host}/ws/socket-server/`);

    // Define event listeners
    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message)

      switch(message['type']){
        case "finding":
          setState("INQUEUE");
          break;
        case 'found':
          break;
        case "playing":
          console.log(message["player to make move"]);
          console.log(name);
          if(message["player to make move"] == name){
            setState("MOVE");
            setInfo("It is your turn to move");
          }
          else{
            setState("HOLD");
            setInfo("Opponent is making a move");
          }
          // break;
        
        // case 'update_board':
          // setBoard(message['board'])
          console.log(message['board']);
          console.log(message['board'].split(''));

          const new_board = message['board'].split('');

          for(let i=0; i < message['board'].length; i++){
            if(new_board[i] == '-'){
              new_board[i] = "";
            }
          }
          console.log(new_board);
          setBoard(new_board);
          break;

        case 'move not accepted':
          break;
        
        case 'game_over':
          console.log("winner is ", message['winner']);
          setState("IDLE");
          setInfo("game over!");
          break;
        case "game_cancel":
          console.log(message['player left'], 'left');
          setState("IDLE");
          break;
        default:
          break;
      }

    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      // Clean up WebSocket connection
      ws.current.close();
    };
  }, [name, ws]);

  const handleMove = (position) => {

    if(board[position] != ''){
      console.log("this spot already taken");
      return;
    }

    if(state != "MOVE"){
      console.log("not your turn yet")
      return;
    }

    ws.current.send(JSON.stringify({
      'type' : 'make-move',
      'position':position,
      'name' : name
    }));
    
  };

  const find_game = () => {
    ws.current.send(JSON.stringify({
      'type' : 'find-game',
      'name' : name
    }));
  }

  const stop_find = () => {
    ws.current.send(JSON.stringify({
      'type' : 'stop-find',
      'name' : name
    }));
  }

  const exit_game = () => {
    ws.current.send(JSON.stringify({
      'type' : 'exit-game',
      'name' : name
    }));
  }

  const handleButton = () => {
    switch(state){
      case "IDLE":
        if(name.length == 0){
          setAlert("Please enter a name");
        }
        find_game();
        break;
      case "INQUEUE":
        stop_find();
        break;
      default:
        exit_game();
        break;
    }
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', p: 2 }}>
      <Typography variant="h4" gutterBottom>Chat Interface</Typography>
      <Board board={board} handleMove={handleMove}/>
      <TextField
        onChange={(event) => {setName(event.target.value)}}
      />
      <Button variant="contained" color="primary" onClick={handleButton} sx={{ ml: 1 }}>
        {state == "IDLE" ? "Find game" : (state == "INQUEUE" ? "Stop looking" : "")}
      </Button>
      {info}
      <Zoom in={alert.length > 0}>
        <Alert>
          {alert}
        </Alert>
      </Zoom>
      
    </Box>
  );
};

export default Home;
