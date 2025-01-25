

let video = document.querySelector(".videoElement");

if (navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({video: true})
    .then (function (stream){
        document.querySelector(".videoElement").srcObject = stream
    })
    .catch (function (error){
        console.log(error)
    })
}
else{
    console.log("hello")
}

    




