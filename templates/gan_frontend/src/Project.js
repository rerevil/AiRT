import Header from "./header.js"
import game from './game.png';
import read from './read.png';
import art from './art.png';
import notif from './notif.png';
import sms from './sms.jpg';
import email from './sms.png';
import mountain from './mountain.gif';
import dog from './dog.gif';
import cat from './cat.gif';
import bird from './bird.gif';
import sea from './sea.gif';
import face from './face.gif';
import before from './beforeesr.png';
import after from './afteresr.png';
import { Box, Grid, Paper, BoxProps, Modal } from "@mui/material";
import React from "react";


const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };
function Item(props) {
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




export default function Project() {
    const [open, setOpen] = React.useState(false);
    const [passion, setPassion] = React.useState({
        title: "Title",
        description: "Hello World!"
    });
    const dictionary = {
        Videogioco: "L’idea  che coinvolge un videogioco è cosa nuova per me, durante il periodo delle superiori, molto spesso, mi metto a creare un gioco con un concetto molto semplice e applicavo degli algoritmi per automatizzare il lavoro.",
        Lettura: "L’idea che coinvolge la lettura , è quello di poter generare una storia coincisa e coinvolgente.",
        Arte: "L’idea che coinvolge l'arte digitale, è quello di poter generare un'illustrazione visualmente attraente e affascinante.",
        Notifica: `Le notifiche da browser, a primo avviso, possono sembrare una buona soluzione,
        dato che richiede il minimo sforzo dall’utenza. Ma analizzando il caso pi attentamente, è possibile notare che queste notifiche sono poco conosciute dalle persone,
        e renderebbero molto difficile la consegna dell’immagine dato che per essere notificato. Oltre a ciò, è necessario usare lo stesso dispositivo e lo stesso browser.
        `,
        SMS: `Gli SMS sono un’opzione molto particolare e molto conflittuale per via del
        fatto che è il metodo più semplice per far ricevere all'utente la loro immagine
        richiesta. Ma ciò si può complicare facilmente perché i clienti potrebbero sentirsi
        scettici dall’affidare il proprio numero di telefono a un sito che non dovrebbe necessitarne. C'è anche da considerare che l’utente ha la necessità di possedere una
        SIM con un numero e un dispositivo che possa usarla. Sarà necessaria anche dalla
        mia parte possedere una SIM internazionale con messaggi illimitati, e ciò lo rende
        ai miei occhi un’opzione che ha più contro che pro
        `,
        Email: `L’opzione della spedizione via e-mail è la soluzione migliore. L’utente per
        accedere al servizio ha la necessità di procedere con la registrazione in cui è incluso
        un indirizzo e-mail. Non hai la necessità di possedere di un dispositivo particolare
        per ricevere l’immagine, è possibile accedere da qualsiasi dispositivo collegato a
        internet. E anche più semplice per quanto riguarda il mio lato, dato che tutto ciò 
        che ho bisogno è semplicemente una e-mail.
        `

    }

    const handleOpen = (prompt) => {
        console.log(dictionary[prompt])
        setPassion({title: prompt, description: dictionary[prompt]});
        setOpen(true)};
    const handleClose = () => setOpen(false);
    return  <>
    <Header/>
    <div>
        <h1 style={{'padding-top': '50px'}}>Idea</h1>
        <p>Per il tema del progetto, mi sono rivolto alle mie passioni personali.</p>
    <Box   sx={{
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gridAutoRows: '150px',
    gap: 1,
  }}>
    <Item onClick={() => {handleOpen("Videogioco")}}>
    <p>
    Videogioco
        </p>
        <img src={game} height="50px" />
        </Item>
    <Item onClick={() => {handleOpen("Lettura")}}>
    
        <p>
        Lettura
        </p>
        <img src={read} height="50px" />
        </Item>

        <Item onClick={() => {handleOpen("Arte")}}>
    
    <p>
    Arte digitale
    </p>
    <img src={art} height="50px" />
    </Item>
</Box>
  <h1>L'applicazione web</h1>
  <p>
    Ho deciso di realizzare una applicazione web che dato un
soggetto, grazie all’intelligenza artificiale (AI), sarà possibile generare arte (ART),
finendo così con una fusione tra AI e ART, diventando in questo modo AiRT. <br />
Ho pensato, come business idea, quella
di implementare un servizio ad iscrizione, in cui è possibile avere una quantità
superiore di immagini giornaliere e di migliore qualità. Quest'ultima però non è ancora effettivamente completata.
  </p>
  <h4>Gestione dei tempi</h4>
  <p>
    Per la generazione delle immagini, l'applicazione si affida a modelli di rete neurali già allenati, perciò, nel caso in cui è necessario allenare 
    un nuovo modello, è inevitabile che l’utente debba aspettare un lasso di tempo eccessivamente lungo. <br />
    Per risolvere questo problema sono disponibili molteplici
approcci:
  </p>
  
  <Box   sx={{
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gridAutoRows: '150px',
    gap: 1,
  }}>
    <Item onClick={() => {handleOpen("Notifica")}}>
    <p>
    Notifica
        </p>
        <img src={notif} height="50px" />
        </Item>
    <Item onClick={() => {handleOpen("SMS")}}>
    
        <p>
        SMS
        </p>
        <img src={sms} height="50px" />
        </Item>

        <Item onClick={() => {handleOpen("Email")}}>
    
    <p>
    Email
    </p>
    <img src={email} height="50px" />
    </Item>
</Box>

<h1>Concorrenza</h1>
  <p>
  Il competitor più rilevante che conosco è <a href="https://openai.com/dall-e-2/" target="_blank">Dall-E</a>. <br />
  Dall-E è un programma sviluppato da OpenAi, che recentemente ha ricevuto fama
per via di una nuova versione rilasciata denominata Dall-E2.
Questa intelligenza artificiale è stata creata con in mente l’idea di creare delle
immagini partendo da una didascalia testuale per ottenere un’ampia gamma di
concetti esprimibili in linguaggio naturale. Dall-E utilizza versione di 12B di
parametri dal modello del GPT-3 per la comprensione del testo e in questo modo,
tenta di generare una plausibile l’immagine di ciò che è stato descritto.

  </p>

<h1>
Dataset
</h1>
<p>
Per il dataset, la strategia che verrà utilizzato è il web-scrapping. Perciò, l’operazione
che farà il programma è quello di andare ad estrarre immagini da siti web. Più
specificatamente, il dataset sarà composto da immagini prese da un sito chiamato <a href="https://www.freeimages.com/image" target="_blank">freeimages</a>, perciò libero da qualsiasi problemi di diritto d’autore.
  </p>

  <h1>GAN</h1>
<p>
  Per la generazione delle immagini, ho utilizzato una rete
neurale chiamata Generative Adversarial Network, meglio conosciuto come GANs. <br />
La GANs è un tipo di modello di deep learning senza supervisione.
Il funzionamento di questa rete neurale è quello di generare nuovi campioni partendo da un grande insieme di dati. Nello specifico, la GAN è composta da due
reti neurali: il generatore e il discriminatore
</p>

<Box   sx={{
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gridAutoRows: '300px',
    gap: 1,
  }}>
    <Item>
      <p> Dog </p>
      <img src={dog} height="200px" />
    </Item>

    <Item>
      <p> Cat </p>
      <img src={cat} height="200px" />
    </Item>

    <Item>
      <p> Bird </p>
      <img src={bird} height="200px" />
    </Item>

    <Item>
      <p> Face </p>
      <img src={face} height="200px" />
    </Item>

    <Item>
      <p> Sea </p>
      <img src={sea} height="200px" />
    </Item>

    <Item>
      <p> Mountain </p>
      <img src={mountain} height="200px" />
    </Item>
</Box>

  <h1>ESRGAN</h1>
  <p>
  Per l’ingrandimento dell’immagine invece, ho utilizzato un’altra rete neurale dal
nome Enhanced Super-Resolution Generative Adversarial Networks (ESRGAN).
ESRGAN è una tecnica di upscaling che permette non solo di ingrandire l’immagine
ma di migliorarne la qualità.
  </p>
  <Box   sx={{
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gridAutoRows: '300px',
    gap: 1,
  }}>
  <Item>
      <p> Prima </p>
      <img src={before} height="200px" />
    </Item>

    <Item>
      <p> Dopo </p>
      <img src={after} height="200px" />
    </Item>
</Box>
    </div>
    <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <h2>
            {passion.title}
          </h2>
          <p>
            {passion.description}
          </p>
        </Box>
      </Modal>
    </>

}