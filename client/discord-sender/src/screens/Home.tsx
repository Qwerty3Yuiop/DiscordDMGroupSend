import { useState } from 'react'
import './Home.css'

function Homepage() {
  const [discordToken, setDiscordToken] = useState('');
  const [channelId, setChannelId] = useState('');
  const [showPasswordPrompt, setShowPasswordPrompt] = useState(false);
  const [password, setPassword] = useState('');

  const searchChannelId = () => {
    const token = localStorage.getItem('DiscordSenderEncryptedToken');
    if (discordToken && token) {
      setShowPasswordPrompt(true);
      setPassword('');
    } else {
      alert('Please set your Discord token in the settings first.');
    }
  }

  const handlePasswordSubmit = () => {
    const token = localStorage.getItem('DiscordSenderEncryptedToken');
    if (token) {
      try {
        const tokenCharCode = token.split('-').map(Number);
        let trueToken = "";
        for (let i = 0; i < tokenCharCode.length; i++) {
          trueToken += String.fromCharCode(tokenCharCode[i] - password.charCodeAt(i % password.length));
        }
        setDiscordToken(trueToken);
        
      } catch (error) {
        alert('Invalid password or token.');
      }
      setShowPasswordPrompt(false);
    }
  }

  const handlePasswordCancel = () => {
    setShowPasswordPrompt(false);
    setPassword('');
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Channel ID"
        value={channelId}
        onChange={(e) => setChannelId(e.target.value)}
      />
      <button
        onClick={searchChannelId}>Search Channel
      </button>
      
      {showPasswordPrompt && (
        <div className='fixed-div'>
          <div className='password-input'>
            <h3>Enter Password</h3>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div>
              <button onClick={handlePasswordCancel}>Cancel</button>
              <button onClick={handlePasswordSubmit} disabled={!password}>
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>)
}

export default Homepage
