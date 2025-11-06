import { Routes, Route } from 'react-router-dom'
import { ThemeProvider } from 'styled-components'
import GlobalStyle from './styles/GlobalStyle'
import theme from './styles/theme'
import Layout from './components/Layout'
import Home from './pages/Home'
import Mission from './pages/Mission'
import Profile from './pages/Profile'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/mission" element={<Mission />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Layout>
    </ThemeProvider>
  )
}

export default App