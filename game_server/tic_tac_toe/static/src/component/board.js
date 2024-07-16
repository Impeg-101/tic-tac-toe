import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, List, ListItem, ListItemText, Typography, Grid, Zoom } from '@mui/material';

export default function Board({board, handleMove}){

    const get_tile = (position, borderLeft, borderRight) => {
        return (
            <Grid item xs={4} 
                height={150}
                width={150} 
                onClick={()=>{handleMove(position)}} 
                sx={{
                ":hover": {
                  cursor: 'pointer'
                },
                borderLeft: borderLeft ? 10 : 'none',
                borderRight: borderRight ? 10 : 'none',
                borderColor: '#90d5ff',
                justifyContent: "center"
              }}>
                <Zoom in style={{ transitionDelay: '1000ms'}}>
                    <Typography
                        fontSize={100}
                        fontWeight={1000}
                        color={"#fcfca9"}
                    >{board[position]}</Typography>
                </Zoom> 
            </Grid>
        )
    }

    return (<>
    <Box 
        padding={2}
        margin={1}
        sx={{
            backgroundColor : "#634b9c",
            borderRadius: 20
        }}
    >
        <Grid container height={489} width={489}>
            <Grid container item xs={12} borderBottom={10} borderColor={'#90d5ff'}>
                {get_tile(0, false, true)}
                {get_tile(1, true, true)}
                {get_tile(2, true, false)}
            </Grid>
            <Grid container item xs={12} borderTop={10} borderBottom={10} borderColor={'#90d5ff'}>
                {get_tile(3, false, true)}
                {get_tile(4, true, true)}
                {get_tile(5, true, false)}
            </Grid>
            <Grid container item xs={12} borderTop={10} borderColor={'#90d5ff'}>
                {get_tile(6, false, true)}
                {get_tile(7, true, true)}
                {get_tile(8, true, false)}
            </Grid>
        </Grid>
    </Box>
        
    </>)
}
