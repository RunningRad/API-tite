import React, { useState } from 'react';
import './Chat.css';
import ChatGPTImage from './images/chatgpt.svg';
import axios from 'axios';
import ListGroup from './components/ListGroup';
import CustomAccordion from './components/Accordion';


const App = () => {
  const ts = new Date();
  const [chatGptMessage, setChatGptMessage] = useState({
    sender: "ChatGPT",
    msg: "Hi! What would you like to eat today?",
    ts: `${ts.getHours()}:${ts.getMinutes()}`
  });
  const [newUserInput, setNewUserInput] = useState('');

  const [stores, setStores] = useState([{
    name: 'Options will appear here',
    description: ['description']
  }]) 

  const handleInputChange = (e) => {
    setNewUserInput(e.target.value);
  };

  const handleUserRequest = async (e) => {
    e.preventDefault();
    if (newUserInput.trim() === '') return;

    try {
      // Send user's input to the backend API
      const response = await axios.get(`http://localhost:8000/ask?q=${encodeURIComponent(newUserInput)}`);
      console.log(response)
      const ts = new Date();
      setChatGptMessage({
        sender: "ChatGPT",
        msg: response.data.text,
        ts: `${ts.getHours()}:${ts.getMinutes()}`
      });
      setStores(response.data.store_options)
    } catch (error) {
      console.error("Error fetching response from API:", error);
    }

    // Clear the input field
    setNewUserInput('');
  };

  return (
    <section className="msger">
      <header className="msger-header">
        <div className="msger-header-title">
          <i className="fas fa-comment-alt"></i> API-tite
        </div>
        <div className="msger-header-options">
          <span><i className="fas fa-cog"></i></span>
        </div>
      </header>
      <main className="msger-chat">
        <div className="msg left-msg">
          <div
            className="msg-img"
            style={{ backgroundImage: `url(${ChatGPTImage})` }}
          ></div>
          <div className="msg-bubble">
            <div className="msg-info">
              <div className="msg-info-name">ChatGPT</div>
              <div className="msg-info-time">{chatGptMessage.ts}</div>
            </div>
            <div className="msg-text">{chatGptMessage.msg}</div>
          </div>
        </div>
      </main>
      <form className="msger-inputarea" onSubmit={handleUserRequest}>
        <input
          value={newUserInput}
          onChange={handleInputChange}
          type="text"
          className="msger-input"
          placeholder="Enter your message..."
        />
        <button className="msger-send-btn">Send</button>
      </form>     
     <CustomAccordion storeData={stores} />
    </section>
  );
};

export default App;
