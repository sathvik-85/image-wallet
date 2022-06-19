import {useEffect,useState} from "react";
import * as React from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DesktopDateTimePicker } from '@mui/x-date-pickers/DesktopDateTimePicker';
import Stack from '@mui/material/Stack';
import axios from "axios"


function App() {

  const [fetchdata,setFetchdata] = useState(false);
  const [data, setData] = useState([]);
  const [value, setValue] = React.useState(new Date(Date.now()));
  const [files, setFiles] = useState()
let url = window.location.hostname 


const onSubmitHandler =(e) =>{
e.preventDefault();
const timestamp = Date.parse(value)/1000;


  const formData = new FormData();

  for (const file of e.target.files.files){

    formData.append("files",file)
  }

console.log(formData)
  

  
axios.post(`http://localhost:8080/uploadfile?date=${timestamp}`,formData)


}


 

  useEffect(() =>{
    
    fetch("http://localhost:8080/image-gallery").then(data => data.json()).then(pathData => setData(pathData) )
  },[fetchdata])



  
  return (
    <>

    <div>
      <form onSubmit={onSubmitHandler}>
        <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Stack spacing={3}>
        <DesktopDateTimePicker
          label="For desktop"
          value={value}
          onChange={(newValue) => {
            setValue(newValue);
          }}
          renderInput={(params) => <TextField {...params} />}
        />
      </Stack>
    </LocalizationProvider>
    <input type="file" name="files"  multiple/>
    <button type="submit" >Submit Image&time</button>
    </form>
    </div>
    <div className="App">
      <hr />
      <center><bold><h1>Image Gallery</h1></bold></center>
      <button onClick={() => setFetchdata(!fetchdata) }>fetch</button>
      <div className="box">
      {data.map(image => {
       return (
        
            
           
       <img src={`http://localhost:8080${image.path}`}  width="300px" height="300px" />
       

     
  
        )
      })}
</div>
    </div>

    </>
  );
}

export default App;
