import { useState, useEffect } from 'react'
import './Settings.css'

function Settingspage() {
  // Token params
  const [encryptedDiscordToken, setEncryptedDiscordToken] = useState('');
  const [rawDiscordToken, setRawDiscordToken] = useState<string | null>(null);

  // Channel ID
  const [channelId, setChannelId] = useState('');

  // Password Menu
  const [showPasswordPrompt, setShowPasswordPrompt] = useState(false);
  const [password, setPassword] = useState('');
  

  useEffect(() => {
    const storedToken = localStorage.getItem('DiscordSenderEncryptedToken');
    if (storedToken) {
      setEncryptedDiscordToken(storedToken);
    }
  }, []);
  
  

  const handleTokenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRawDiscordToken(e.target.value);
  };

  const handlePasswordSubmit = () => {
    // Here you would encrypt pendingToken with password and store it
    setEncryptedDiscordToken(rawDiscordToken || '');
    setShowPasswordPrompt(false);
    setPassword('');
    setRawDiscordToken(null);
  };

  const handlePasswordCancel = () => {
    setShowPasswordPrompt(false);
    setPassword('');
    setRawDiscordToken(null);
  };

  const tokenSubmit = () => {
    setShowPasswordPrompt(true);
  }

  return (
    <div>
      <h1>Settings</h1>
      <div className="settings-container">
        <table className="settings-table">
          <tbody>
            <tr>
              <td className="settings-label">Discord Token:</td>
              <td className="settings-label">
                <input
                  className = "setting-input"
                  type="password"
                  placeholder="Discord Token"
                  value={encryptedDiscordToken}
                  onChange={handleTokenChange}
                />
                <button className="setting-button" onClick={tokenSubmit}>Submit</button>
              </td>
              <td className="settings-label"></td>
              <td className="settings-label"></td>
            </tr>
            <tr>
              <td className="settings-label">Primary Channel ID:</td>
              <td className="settings-label">
                <input
                  className="setting-input"
                  type="text"
                  placeholder="Channel ID"
                  value={channelId}
                  onChange={(e) => setChannelId(e.target.value)}
                />
              </td>
              <td className="settings-label"></td>
              <td className="settings-label"></td>
            </tr>
          </tbody>
        </table>
        
        

      </div>
      

    {showPasswordPrompt && (
      <div className="password-modal">
        <div className="password-input">
          <h3>Enter Password</h3>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <div className="password-input-buttons">
            <button className="password-button" onClick={handlePasswordCancel}>Cancel</button>
            <button className="password-button" onClick={handlePasswordSubmit} disabled={!password}>
              Submit
            </button>
          </div>
        </div>
      </div>
    )}
  </div>)
}

export default Settingspage
