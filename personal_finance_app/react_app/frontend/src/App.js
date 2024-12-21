import React from 'react';
import UploadForm from './components/UploadForm';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div>
      <h1>Excel Data Processor</h1>
      <UploadForm />
      <Dashboard />
    </div>
  );
}

export default App;
