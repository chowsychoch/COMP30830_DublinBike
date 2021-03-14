fetch("/station").then(response =>{
    let data = response.json();
    console.log("data: ",data);
}).catch(err =>{
    console.log("OOPS",err);
})
