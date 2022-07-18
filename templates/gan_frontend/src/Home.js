import React, { useEffect, useState } from "react";
import CircularProgress from '@mui/material/CircularProgress';
import {Stack, Button, TextField  } from "@mui/material"
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import mail_img from './mail.png'
import Footer from './Footer.js';
import Header from "./header.js"

const imageUrl = "http://127.0.0.1:5000/generate_image";


export default function Home() {
    const [img, setImg] = useState(null);
    const [text, setText] = useState('');
    const [path, setPath] = useState('');
    const auth = localStorage.getItem('auth')
    
    const fetchImage = () => {
        
        const options = {
            method: "POST",
            headers: new Headers({'Authorization': auth}),
        };

        fetch(`http://127.0.0.1:5000/generate_image?search=${text}`, options)
        .then((response) =>{ 
            console.log(response);
            return response.json()}).then((data) => {
            if (data === 201){
                setImg(mail_img)
                window.alert('The model has successfully started training, the result will be sent via email.')}
            else
                setPath(data.path);
          })
        //const imageBlob = await res.blob();
        //const imageObjectURL = URL.createObjectURL(imageBlob);
        //setImg(imageObjectURL);
      };

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/images/${path}`)
        .then(response => response.blob())
        .then(imageBlob => {
            const imageObjectURL = URL.createObjectURL(imageBlob);
            setImg(imageObjectURL);})
    }, [path])

    const handleChange = (value) => {
        setText(value)
    }

    const fiterText = (value) => {
        if (value.split(" ").length > 1){
            window.alert('Please, enter a single word')
            return
        }
        if (!value){
            window.alert('Please, enter a word')
            return
        }
        console.log(auth)
        if (!auth){
            window.alert('Please, Login')
            return
        }
        setImg(null)
        fetchImage()
    }

    return (<>
    
    <Header/>
        <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
            <Box
  container
  spacing={2}
  direction="column"
  alignItems="center"
  justifyContent="center"
  >
             
            <Grid item xs={5}>
                 {img ? <img src={img} alt="image"width={250} height={250} border="1 black" /> : <Stack alignItems="center">
<CircularProgress size='20vh'/></Stack>
}
             </Grid>
             
            <Grid item xs={3} pt={5}>
                <TextField 
                onChange={(event) => {handleChange(event.target.value)}}
                />
            </Grid>
            <Grid item xs={2} pt={2}>
                <Button variant="contained" onClick={()  => {fiterText(text)}}>Generate</Button>
            </Grid>

            </Box>

      </div>
            <Footer/>
      </>
    );
  }