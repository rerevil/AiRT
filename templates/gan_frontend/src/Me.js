import Header from "./header.js"
import opcua from './opcua.jpg';
import db from './db.png';
import api from './api.png';
import { Box, Grid, Paper, BoxProps } from "@mui/material";

function Item(props: BoxProps) {
    const { sx, ...other } = props;
    return (
      <Box
        sx={{
          bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#101010' : '#fff'),
          color: (theme) => (theme.palette.mode === 'dark' ? 'grey.300' : 'grey.800'),
          border: '1px solid',
          borderColor: (theme) =>
            theme.palette.mode === 'dark' ? 'grey.800' : 'grey.300',
          p: 1,
          borderRadius: 2,
          textAlign: 'center',
          fontSize: '0.875rem',
          fontWeight: '700',
          ...sx,
        }}
        {...other}
      />
    );
  }

export default function Me() {
    return <>
    <Header/>
    <div>   
        <h1 style={{'padding-top': '50px'}}>Studente</h1>
        <p>
        Sono Renz Joshua Villanueva, ho 21 anni e vivo a Milano (MI) e ho un grande
interesse nella programmazione e per questo motivo ho intenzione di avere una
carriera nel settore informatico. <br/>
Ho sempre avuto un interesse sul mondo tecnologico e per questo motivo, per la scelta delle scuole superiori, ho deciso di frequentare la scuola di secondo grado superiore Luigi
Lagrange. <br/>
Il mio obiettivo è quello di essere riconosciuto come una persona con una profonda conoscenza sull’informatica così da poter essere una figura d’ispirazione ai
ragazzi che hanno, come me, una passione in questo settore.
        </p>
        <h1>Azienda</h1>
        <p>
        L’azienda che mi accolto per il tirocinio e in cui svolto lo stage è chiamata Ice-flex. <br />
         Ice-flex è una azienda che sviluppa sistemi e software dedicate al supporto
dell’industria 4.0, specialmente nel campo delle lavorazioni plastiche.<br />
In azienda, ho sviluppato molte funzionalità di web app per software dedicate

all’industria 4.0 in cui: <br /><br /></p>
    <Box   sx={{
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gridAutoRows: '400px',
    gap: 1,
  }}>
    <Item>
    <p>
La gestione della connessione di macchina al proprio dispositivo, tramite un protocollo chiamato OPCUA.
        </p>
        <img src={opcua} height="300px" />
        </Item>
    <Item>
    
        <p>
        La gestione delle interrogazioni SQL ad un database
        </p>
        <img src={db} height="300px" />
        </Item>
    <Item>
    
<p>
        La creazione di API
        </p>
        <img src={api} height="300px" />
        </Item>

</Box>
    </div>
    </>

}