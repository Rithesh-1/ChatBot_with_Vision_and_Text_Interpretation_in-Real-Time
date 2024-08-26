import React,{useState} from 'react';
import axios from 'axios';
import webcam from 'react-webcam';
import './App.css';

function App(){
    const [question,setQuestion] = useState('');
    const [contextType,setContextType] = useState('pdf');
    const [contextSource,setContextSource] = useState('');
    const [answer,setAnswer] =useState('');
    const [context,setContext] = useState('');
    const [accessToken,setAccessToken] = useState('');
    const webcamRef = React.useRef(null);

    const handlelogin = async() =>{
        try{
            const response = await axios.post('/login',{username:'test',password:'test'});
            setAccessToken(response.data.accessToken);
        }catch(error){
            console.error('Login Failed',error);
        }
    };
    const handleSubmit = async(e) =>{
        e.preventDefault();
        try{
            const response = await axios.post('/ask',{
                question,
                context_type :contextType,
                context_source: contextSource
            },{
                headers:{Authorization: `Bearer ${accessToken}`}
            });
            setAnswer(response.data.answer);
        }catch(error){
            console.error('Error asking question',error);
        }
    };
    const capture = React.useCallback(async() =>{
        const imageSrc =webcamRef.current.getScreenshot();
        const blob = await fetch(imageSrc).then(res=>res.blob());
        const formData = new FormData();
        formData.append('image',blob,'capture.png');
        try{
            const response = await axios.post('/upload-image',formData,{
                headers:{
                    'Content-Type':'multipart/form-data',
                    Authorization: `Bearer ${accessToken}`
                }
            });
            setContext(response.data.context);
        }catch (error){
            console.error('Error uploading image',error);
        }

    },[webcamRef,accessToken]);
    
    return (
        <div className="App" >
            <h1>Chatbot</h1>
            <button onClick={handlelogin}>Login</button>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Question:</label>
                    <input 
                    type ="text"
                    value ={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    required
                    />
                </div>
                <div>
                    <label>Context Type:</label>
                    <select
                    value={contextType}
                    onChange={(e) => setContextType(e.target,value)}
                    >
                        <option value="pdf">PDF</option>
                        <option value="csv">CSV</option>
                        <option value="url">URL</option>
                        <option value="image">Image</option>
                    </select>
                </div>
                {contextType == 'image'?(
                    <div>
                        <webcam
                          audio ={false}
                          ref={webcamRef}
                          screenshotFormat="image/jpeg"
                        />
                        <button type="button" onClick={capture}>Capture Image</button>
                        {context &&(
                            <div>
                                <h2>Extracted Context:</h2>
                                <p>{context}</p>
                            </div>
                        )}
                    </div>
                ) :(
                    <div>
                        <label>Context Source</label>
                        <input 
                            type="text"
                            value={contextSource}
                            onChange={(e)=> setContextSource(e.target.value)}
                            required
                        />
                    </div>
                )}
                <button type='submit'>Ask</button>
            </form>
            {answer &&(
                <div>
                    <h2>Answer:</h2>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
}
export default App;