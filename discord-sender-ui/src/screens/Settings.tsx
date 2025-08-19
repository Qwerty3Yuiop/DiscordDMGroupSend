import { useState, useEffect } from 'react'
import './Settings.css'

function Settingspage() {
  // Token params
  const [displayDiscordToken, setDisplayDiscordToken] = useState('');

  // Channel ID
  const [channelId, setChannelId] = useState('');

  // Password Menu
  const [showPasswordPrompt, setShowPasswordPrompt] = useState(false);
  const [password, setPassword] = useState('');
  

  useEffect(() => {
    const storedToken = localStorage.getItem('DiscordSenderEncryptedToken');
    if (storedToken) {
      setDisplayDiscordToken(storedToken);
    }
  }, []);
  
  

  const handleTokenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDisplayDiscordToken(e.target.value);
  };

  const handlePasswordSubmit = () => {
    if (password === '') {
      localStorage.setItem('DiscordSenderEncryptedToken', displayDiscordToken);
      setShowPasswordPrompt(false);
      setPassword('');
      return;
    }
    try {
      const encryptToken = async () => {
        const enc = new TextEncoder();
        const keyMaterial = await window.crypto.subtle.importKey(
          'raw',
          enc.encode(password),
          { name: 'PBKDF2' },
          false,
          ['deriveKey']
        );
        const salt = window.crypto.getRandomValues(new Uint8Array(16));
        const key = await window.crypto.subtle.deriveKey(
          {
            name: 'PBKDF2',
            salt,
            iterations: 100000,
            hash: 'SHA-256',
          },
          keyMaterial,
          { name: 'AES-GCM', length: 256 },
          true,
          ['encrypt']
        );
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const ciphertext = await window.crypto.subtle.encrypt(
          {
            name: 'AES-GCM',
            iv,
          },
          key,
          enc.encode(displayDiscordToken)
        );
        // Store salt, iv, and ciphertext as base64
        const b64 = (buf: ArrayBuffer) => btoa(String.fromCharCode(...new Uint8Array(buf)));
        const encryptedData = JSON.stringify({
          salt: b64(salt),
          iv: b64(iv),
          ciphertext: b64(ciphertext),
        });
        localStorage.setItem('DiscordSenderEncryptedToken', encryptedData);
        setDisplayDiscordToken(encryptedData);
      };
      encryptToken();
    } catch (e) {
      alert('Encryption failed.');
    }
    setShowPasswordPrompt(false);
    setPassword('');
  };

  const handlePasswordCancel = () => {
    setShowPasswordPrompt(false);
    setPassword('');
    setDisplayDiscordToken('');
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
                  value={displayDiscordToken}
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
