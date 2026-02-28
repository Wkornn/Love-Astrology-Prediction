import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BirthDataProvider } from './context/BirthDataContext';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import Mode1Page from './pages/Mode1Page';
import Mode2Page from './pages/Mode2Page';
import Mode3Page from './pages/Mode3Page';

function App() {
  return (
    <BirthDataProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/mode1" element={<Mode1Page />} />
            <Route path="/mode2" element={<Mode2Page />} />
            <Route path="/mode3" element={<Mode3Page />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </BirthDataProvider>
  );
}

export default App;
