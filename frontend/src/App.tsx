import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { BrowserRouter, Routes, Route } from 'react-router';
import { Layout } from './components/Layout/Layout';
import { InterviewPage } from './pages/InterviewPage';
import { HistoryPage } from './pages/HistoryPage';
import { ProfilePage } from './pages/ProfilePage';
import './index.css';

// Создаем Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 минут
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="App">
          <Routes>
            <Route path="/" element={<Layout />}>
              {/* Главная страница - интервью */}
              <Route index element={<InterviewPage />} />
              
              {/* Дополнительные страницы */}
              <Route path="history" element={<HistoryPage />} />
              <Route path="profile" element={<ProfilePage />} />
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
      
      {/* React Query DevTools (только в development) */}
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}

export default App;
