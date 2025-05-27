import { useState, useEffect } from 'react'
import './Settings.css'

function Settingspage() {
  const [discordToken, setDiscordToken] = useState('');

  useEffect(() => {
    const storedToken = localStorage.getItem('DiscordSenderEncryptedToken');
    if (storedToken) {
      setDiscordToken(storedToken);
    }
  }, []);
  
  const [channelId, setChannelId] = useState('');

  const [showPasswordPrompt, setShowPasswordPrompt] = useState(false);
  const [password, setPassword] = useState('');
  const [pendingToken, setPendingToken] = useState<string | null>(null);

  const handleTokenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPendingToken(e.target.value);
    setShowPasswordPrompt(true);
  };

  const handlePasswordSubmit = () => {
    // Here you would encrypt pendingToken with password and store it
    setDiscordToken(pendingToken || '');
    setShowPasswordPrompt(false);
    setPassword('');
    setPendingToken(null);
  };

  const handlePasswordCancel = () => {
    setShowPasswordPrompt(false);
    setPassword('');
    setPendingToken(null);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Discord Token"
        value={discordToken}
        onChange={handleTokenChange}
      />
      <input
        type="text"
        placeholder="Channel ID"
        value={channelId}
      onChange={(e) => setChannelId(e.target.value)}
    />

    {showPasswordPrompt && (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0,0,0,0.5)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
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

export default Settingspage
