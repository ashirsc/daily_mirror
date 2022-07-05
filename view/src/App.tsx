import './App.css'

import { useEffect, useState } from 'react'

import Gallery from 'react-photo-gallery'
import logo from './logo.svg'

function App() {
  const [count, setCount] = useState(0)
  const [photos, setPhotos] = useState([])

  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsLoading(false)
    fetch("http://127.0.0.1:8000/all").then(async raw => {
      const res = await raw.json()
      const pics = res.files.map((file:string) => { return {src:"http://127.0.0.1:8000/images/" + file}})
      setPhotos(pics)

    })
  
   
  }, [])
  

  return (
    <>
    <h1>Your photos</h1>
    <Gallery photos={photos} />
    </>
  )
}

export default App
