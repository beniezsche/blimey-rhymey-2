import { useState , useEffect} from 'react';

export function MainTab() {

  const [headlines, setHeadlines] = useState([])

  useEffect(() => {

    fetch(
      'http://127.0.0.1:8000/v1/headlines/all', {

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
        setHeadlines(res)
      }
    ).catch(
      reason => {
        console.log(reason)
      }
    )

  },[]);

  return (
    <List data={headlines}/>
  )

}

function List({data}) {

  const headlines = []

  data.forEach(element => {
    headlines.push(<ListItem key = {element.id} element={element}/>)
  })

  return (
    // {listItems}
    <table>
      <tbody>
        <tr>
          <td><h2>Headline</h2></td>
          <td><h2>Rhyme</h2></td>
        </tr>
        {headlines}
      </tbody>
    </table>
  )
}


function ListItem ({element}) {

  const [headlineObject, setHeadlineObject] = useState(element)
  const [rhymeObject, setRhymeObject] = useState(element.rhyme)
  const [loadingRhyme, setLoadingRhyme] = useState(false) 


  if (loadingRhyme) {
    return (
      <>
      <tr>
        <td>{headlineObject.headline}</td>
        <td>{rhymeObject}</td>
        <td><button className="hello">Generating ...</button></td>
      </tr>
    </>
    )
  }
  else {
    return (
      <>
      <tr>
        <td>{headlineObject.headline}</td>
        <td>{rhymeObject}</td>
        <td><button className="hello" onClick={() => generateNewRhyme(setRhymeObject, setLoadingRhyme, headlineObject.headline)}>Generate New Rhyme</button></td>
      </tr>
    </>
    )
  }
}

function generateNewRhyme(setRhymeObject, setLoadingRhyme, headline) {

  setLoadingRhyme(true)
  fetch(
    'http://127.0.0.1:8000/v1/headlines/rhyme?' + new URLSearchParams({
      headline: headline,
      user_id: localStorage.getItem('user_id')
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
      setRhymeObject(res)
      setLoadingRhyme(false)
    }
  ).catch(
    reason => {
      console.log(reason)
      setLoadingRhyme(false)
    }
  )
}