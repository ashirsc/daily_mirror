import './App.css'

import { useEffect, useState } from 'react'

import Gallery from 'react-photo-gallery'

function App() {
  const [count, setCount] = useState(0)
  const [photos, setPhotos] = useState([])

  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsLoading(false)
    fetch("/api/all").then(async raw => {
      const res = await raw.json()
      const pics = res.files.map((file:string) => { return {src:"/api/images/" + file}})
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
