// content.js

const constructRequest = (headline) => {
  const requestData = {
    inputs: headline,
    parameters: {
        temperature: 0.50,
        max_tokens: 500,
        top_p:0.95,
        repeat_penalty:1.2, 
        top_k:150,
        echo: false
    }
  };

  return requestData;

}

const getRhymeForHeadline = (requestData, element) => {
  element.innerText = "Rhyming...[ " + element.innerText + " ]"
  chrome.runtime.sendMessage(requestData, response => {
    replaceHeadlineWithRhyme(element, response["generated_text"]);
  });
}

const replaceHeadlineWithRhyme = (element, rhyme) => {
  console.log(rhyme);
  element.innerText = rhyme;
  element.style.color = "#007958"
}

const replaceMainHeadline = () => {

  let headlineElements = document.body.querySelectorAll('h1.hdg1');

  headlineElements.forEach((element) => {
    getRhymeForHeadline(constructRequest(element.innerText) , element);
  })

}

replaceMainHeadline();

