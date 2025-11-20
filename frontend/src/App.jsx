import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import GlobalStyle from './styles/GlobalStyle';
import Layout from './components/Layout';
import Home from './pages/Home';
import Mission from './pages/Mission';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import Welcome from './pages/Welcome';
import { useAuth } from './context/AuthContext';

// 인증이 필요한 라우트를 감싸는 컴포넌트
const ProtectedRoutes = () => {
  const { user } = useAuth();
  return user ? (
    <Layout>
      <Outlet />
    </Layout>
  ) : (
    <Navigate to="/welcome" />
  );
};

// 라우트 정의
const AppRoutes = () => {
  const { user } = useAuth();

  return (
    <Routes>
      {/* 로그인하지 않은 사용자는 Welcome 페이지 표시 */}
      <Route path="/welcome" element={user ? <Navigate to="/" /> : <Welcome />} />
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/" /> : <Register />} />

      <Route element={<ProtectedRoutes />}>
        <Route path="/" element={<Home />} />
        <Route path="/mission" element={<Mission />} />
        <Route path="/profile" element={<Profile />} />
      </Route>

      {/* 알 수 없는 경로 리다이렉트 */}
      <Route path="*" element={user ? <Navigate to="/" /> : <Navigate to="/welcome" />} />
    </Routes>
  );
};


function App() {
  return (
    <>
      <GlobalStyle />
      <AppRoutes />
    </>
  );
}

export default App;