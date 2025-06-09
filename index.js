//Requring module->do it on top
 const express=require("express");
 const ejs=require("ejs");//view engine 
 const path=require("path");
 const exp=require("constants");


 //creating server
 const app=express();
 app.use(express.json());
 //Setting Up EJS
 app.set("view engine","ejs"); //use ejs as view engine

 
 app.use(express.static(path.join(__dirname,"/public")));
 const PORT=3030;//location where this process will run in cpu

 //get request to home page
 app.get("/",(req,res,next)=>{
    res.render("index");
 });
 // we can pass to query to get some info from frontend to backend
 app.get("/search",(req,res)=>{
   const query=req.query;
   console.log(query);
   // res.send(query);

   //TF-IDF algo
   //top 5 problems
   const arr=[
      {
         title:"ABC",
         url:"codeforces.com",
         statement:"great"
      },
      {
         title:"ABC",
         url:"codeforces.com",
         statement:"great"
      },
      {
         title:"ABC",
         url:"codeforces.com",
         statement:"great"
      },
      {
         title:"ABC",
         url:"codeforces.com",
         statement:"great"
      },
      {
         title:"ABC",
         url:"codeforces.com",
         statement:"great"
      }
   ];
   res.json(arr);
 });

 app.listen(PORT,()=>{
    console.log("Server is running on port "+PORT);
 });