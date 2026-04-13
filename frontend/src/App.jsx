import { useState } from 'react'
import axios from 'axios'

function App() {
  const [formData, setFormData] = useState({
    Age: 30,
    Duration: 1,
    Frequency: 2,
    Intensity: 2,
    Vomit: 0,
    Phonophobia: 1
  })

  const [loading, setLoading] = useState(false)
  const [prediction, setPrediction] = useState(null)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseInt(value, 10)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', formData);
      setPrediction(response.data.predicted_type);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  }

  const fields = [
    { name: 'Age', label: 'Age' },
    { name: 'Duration', label: 'Duration' },
    { name: 'Frequency', label: 'Frequency' },
    { name: 'Intensity', label: 'Intensity' },
    { name: 'Vomit', label: 'Vomit' },
    { name: 'Phonophobia', label: 'Phonophobia' }
  ];

  return (
    <>
      <div className="app-container">
        <header>
          <h1>Migraine Predictor AI</h1>
          <p className="subtitle">Clinical Decision Support System</p>
        </header>

        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-grid">
            {fields.map(field => (
              <div key={field.name} className="form-group">
                <label htmlFor={field.name}>{field.label}</label>
                <input
                  type="number"
                  id={field.name}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  required
                />
              </div>
            ))}
          </div>

          {error && <div style={{ color: '#ff4b4b', marginBottom: '20px', textAlign: 'center' }}>Error: {error}</div>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Analyzing...' : 'Predict Migraine Type'}
          </button>
        </form>
      </div>

      {prediction && (
        <div className="result-overlay">
          <div className="result-card">
            <h2>Diagnosis Prediction</h2>
            <p className="prediction-text">{prediction}</p>
            <button className="close-btn" onClick={() => setPrediction(null)}>Close</button>
          </div>
        </div>
      )}
    </>
  )
}

export default App
