import './App.css';
import { useState } from 'react';
import Body from './body';
import StyledEditText from './test';
import query from './api'; // Import the query function

function App() {
  const [userTexts, setUserTexts] = useState([]);
  const handleSubmission = async (responseText, userInput) => { // Add userInput as an argument
    setUserTexts((prevUserTexts) => [...prevUserTexts, { user: userInput, assistant: responseText }]);
  };
  
  return (
    <div>
      <Body texts={userTexts} /> {/* Correct the prop name to texts */}
      <StyledEditText onSubmit={handleSubmission} />
    </div>
  );
}

export default App;

