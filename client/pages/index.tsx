import Head from 'next/head'
import { Inter } from '@next/font/google'
import { useEffect, useState } from 'react'
import FileUploadSingle from '../components/FileUploadSingle'
import FileDownload from '../components/FileDownload'
import axios from 'axios'

export default function Home() {
  const URL = 'http://localhost:8000/api/main'
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(false)

  //Axios GET request
  const getData = () => {
    axios
      .get(URL)
      .then((res: any) => {
        // handle success
        setData(res.data.json())
      })
      .catch((error: any) => {
        // handle error
        console.log(error)
      })
  }

  useEffect(() => {
    getData()
  }, [])

  return (
    <>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="max-w-xl mx-auto justify-center content-center">
        <div className="container max-w-7xl self-center mx-auto pt-16">
          <h1 className="mb-20 text-3xl font-extrabold">
            CEN Zastropovani cen .xlsx -{'>'} .pdf
          </h1>

          <div className="wrapper">
            <h2>1.krok - Vzorový soubor</h2>
            <FileDownload
              fileName="Simple.pdf"
              label="Stáhnout"
              description="Vzorový soubor pro vyplnění dat"
            />
            <hr className="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700"></hr>
          </div>

          <div className="wrapper">
            <h2>2.krok - Nahrát vyplněný soubor</h2>
            <FileUploadSingle />
            <hr className="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700"></hr>
          </div>

          <div className="wrapper">
            <h2>3.krok - Stáhnout vyplněný soubor</h2>
            <FileDownload
              fileName="Simple.pdf"
              label="Download Simple.pdf"
              description="Stáhněte si vygenerovaný soubor"
            />
          </div>
        </div>
      </main>
    </>
  )
}
