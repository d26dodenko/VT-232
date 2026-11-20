import './App.css'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AllRoutes from './routes/Allroutes';
import Navbar from './components/Navbar';
import Footer from './components/Footer';


function App() {
  return (
    <div className=' w-full'>
       <Navbar />
      <AllRoutes />
      <Footer />
      <ToastContainer />
    </div>
  )
}

export default App
