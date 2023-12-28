// background script

const endpoint = 'http://127.0.0.1:8000/v1/headlines/generate_rhyme' //use the ngrok public generated in the colab file

chrome.runtime.onMessage.addListener( function (message, sender, senderResponse) {

    fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': "Bearer " + "a85f357edc7a6b8e4aefad7098722950"
        },
        body: JSON.stringify(message)
    }).then(res => {
        return res.json();
    }).then(res => {
        senderResponse(res);
    })

    return true
});

