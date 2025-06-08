import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router'

import './App.css'
import {HomePage} from './pages/HomePage'
import {NavBar} from './components/NavBar'
import {AddCategoryModal} from './components/AddCategoryModal'

function App() {

    const [showCategoryModal, setShowCategoryModal] = useState(false);
        
    return (
        <>
            <NavBar 
                handleOpenCategoryModal={() => {setShowCategoryModal(true)}}
            />
            <BrowserRouter>
                <Routes>
                    <Route
                        path='/'
                        element={<HomePage />}
                    />
                </Routes>
            </BrowserRouter>
            <AddCategoryModal show={showCategoryModal} handleClose={() => {setShowCategoryModal(false)}}/>
        </>
      )
}

export default App
