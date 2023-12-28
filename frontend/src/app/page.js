"use client";

import { Inter } from 'next/font/google'
import { useState , useEffect} from 'react';
import { MainTab } from './Main/MainTab';
import { setupFirebase } from './firebase-utils';
import { Search, getTopResultsForSearchTerm , SearchResultsTab} from './Search/Search'
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut } from "firebase/auth";

const inter = Inter({ subsets: ['latin'] })

function App() {

  const [tab, setTab] = useState(0)

  const [searchResults, setSearchResults] = useState([])

  const [userSignedIn, setUserSignedIn] = useState(true)

  // useEffect(() => {
  //   setupFirebase();
  // }, [])

  if(userSignedIn) {
    return (
      <>
        <div className='header'>
          <div className='search-bar'>
            <Search
              onSearchButtonClicked = { (queryTerm) => {
                  setTab(1)
                  setSearchResults([])
                  getTopResultsForSearchTerm(queryTerm, setSearchResults)
                }
              }
              onSearchBarCleared = { () => {
                  setTab(0)
                }
              }
            />
          </div>
        </div>
        <Tab
          tab = {tab}
          data = {searchResults}/>
      </>
    )
  }
  else {
    return (
      <SignInPage onSignInClicked = { () => { } }/>
    )
  }
}

function SignInPage({onSignInClicked}) {
  return (
    <div className = "sign-in-page">
      <button className = "sign-in-page-button" onClick = {onSignInClicked}>Sign In With Google</button>
    </div>
  )
}

function Tab({tab, data}) {

  if(tab == 1) {
    return (
      <SearchResultsTab
          data={data}/>
    )
  }  
  else {
    return (
      <>
        <br/>
        <br/>
        <MainTab/>
      </>
    )
  }
}


export default function Home() {
  return (
    <App/>
  )
}

