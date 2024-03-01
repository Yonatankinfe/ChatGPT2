// StyledEditText.js
import './StyledEditText.css';
import React, { useState } from 'react';
import query from './api'; // Import the query function

function StyledEditText({ onSubmit }) {
  const [userInput, setUserInput] = useState("");

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async () => {
    const data = {
      inputs: userInput,
    };

    try {
      const result = await query(data);
      onSubmit(result[0].generated_text, userInput); // Pass userInput as an argument
      setUserInput("");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <div className='container'>
        <input type="text" className="styled-edit-text" placeholder="Enter your prompt here" 
          value={userInput} onChange={handleInputChange} />
        <button className='sendbutton' onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
}

export default StyledEditText;
