import MainPage from './components/MainPage'
import NavBar from './components/NavBar'
import SideBar from './components/SideBar'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
    return (
        <BrowserRouter>
            <div className="flex flex-row h-dvh w-dvh">
                <NavBar />
                <MainPage />
                <SideBar />
            </div>
        </BrowserRouter>
    )
}

export default App
