import { useState } from 'react';

function SearchResultListItem({index, element}) {

  const [searchResult, setSearchResults] = useState(element)

  return (
    <>
        <tr>
            <td key = {searchResult.id}>{searchResult.headline}</td>
        </tr>
    </>
  )
}


export function SearchResultsTab({data}) {

  return (
    <>
      <SearchResultsList data={data}/>
    </>
  )
}

function SearchResultsList({data}) {

  const searchResults = []

  data.forEach((element, index) => {
    searchResults.push(<SearchResultListItem key = {element.id} element={element}/>)
  })

  return (
    <table className='search-result-table'>
        <tbody>
            {searchResults}
        </tbody>
    </table>
  )

}


export function getTopResultsForSearchTerm(searchTerm, updateFunc) {

  fetch(
    'http://127.0.0.1:8000/v1/headlines/search?' + new URLSearchParams({
      searchTerm: searchTerm,
      user_id: localStorage.getItem("user_id")
  }), {
      method: 'GET', 
      headers: {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + process.env.mytoken
      }
    } 
  ).then(
    value => {
      return value.json();
    }
  ).then(
    res => {
      updateFunc(res)
    }
  ).catch(
    reason => {
      console.log(reason)
    }
  )

}

export function Search({onSearchButtonClicked, onSearchBarCleared}) {

  const [queryTerm, setQueryTerm ] = useState("")

  return (
    <>
      <input 
        type="search" 
        id="fname" 
        autoComplete='off'
        name="fname" 
        onInput={ event => {
            setQueryTerm(event.target.value)
            if(event.target.value === "") {
              onSearchBarCleared()
            }
          }
        }>
      </input>
      <button onClick={() => {
          onSearchButtonClicked(queryTerm)
        }
      }>Search</button>
    </>
  )
}