const { createCanvas, loadImage, registerFont } = require('canvas')
const fs = require('fs')
const express= require("express");
var bodyParser = require('body-parser')
const canvas = createCanvas(1920, 1080);
const ctx = canvas.getContext('2d');

// it from css
// @font-face {
//     font-family: 'me_quran1';
//     src: url("me_quran.ttf");
// }
// @font-face {
//     font-family: 'kalpurush';
//     src: url("kalpurush.ttf");
// }
registerFont("./OpenSans.ttf", {family:"open-sans"});
registerFont("./me_quran.ttf", {family:"me_quran1"});
registerFont("./kalpurush.ttf", {family:"kalpurush"});

const wrapText = (ctx, text, x, y, maxWidth, lineHeight) => {
    const words = text.split(/[ ,]/);
    let line = '';
    for (const [index, w] of words.entries()) {
        const testLine = line + w + ' ';
        const metrics = ctx.measureText(testLine);
        const testWidth = metrics.width;
        if (testWidth > maxWidth && index > 0) {
            ctx.fillText(line, x, y);
            line = w + ' ';
            y += lineHeight;
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line, x, y);
}
function dowabck(){
    // #rect6
    ctx.beginPath();
    ctx.strokeStyle = 'rgb(35, 31, 32)';
    ctx.miterLimit = 10;
    ctx.fillStyle = 'rgb(48, 48, 48)';
    ctx.rect(0, 0, 1920, 1080);
    ctx.fill();
    ctx.stroke();
    
// #g20
    ctx.save();
    
// #polygon8
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(0.500000, 561.100000);
    ctx.lineTo(0.500000, 829.500000);
    ctx.lineTo(829.500000, 0.500000);
    ctx.lineTo(561.100000, 0.500000);
    ctx.fill();
    
// #polygon10
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(1903.100000, 0.500000);
    ctx.lineTo(1634.700000, 0.500000);
    ctx.lineTo(554.700000, 1080.500000);
    ctx.lineTo(823.100000, 1080.500000);
    ctx.fill();
    
// #polygon12
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(1366.300000, 0.500000);
    ctx.lineTo(1097.900000, 0.500000);
    ctx.lineTo(17.900000, 1080.500000);
    ctx.lineTo(286.300000, 1080.500000);
    ctx.fill();
    
// #polygon14
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(1920.500000, 519.900000);
    ctx.lineTo(1920.500000, 251.500000);
    ctx.lineTo(1091.500000, 1080.500000);
    ctx.lineTo(1359.900000, 1080.500000);
    ctx.fill();
    
// #polygon16
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(0.500000, 0.500000);
    ctx.lineTo(0.500000, 292.800000);
    ctx.lineTo(292.800000, 0.500000);
    ctx.fill();
    
// #polygon18
    ctx.beginPath();
    ctx.fillStyle = 'rgb(41, 41, 41)';
    ctx.moveTo(1920.500000, 1080.500000);
    ctx.lineTo(1920.500000, 788.200000);
    ctx.lineTo(1628.200000, 1080.500000);
    ctx.fill();
    ctx.restore();
    
// #rect22
    ctx.beginPath();
    ctx.globalAlpha = 0.7;
    ctx.fillStyle = 'rgb(79, 114, 219)';
    ctx.rect(87.500000, 63.000000, 1780.100000, 443.500000);
    ctx.fill();
    
// #rect24
    ctx.beginPath();
    ctx.globalAlpha = 0.7;
    ctx.fillStyle = 'rgb(121, 156, 76)';
    ctx.rect(45.500000, 565.500000, 1780.100000, 443.500000);
    ctx.fill();
    
    ctx.globalAlpha = 1 ;
}

function getfontSizeFrame(text, w, h, family="kalpurush"){
    let fontsize = 100;
    while (1) {
        ctx.font = 'bold '+fontsize+'px '+family;
        let metrics = ctx.measureText(text);
        let sizmaxw = metrics.width;
        let maxlines = sizmaxw/w;
        let maxh  = metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent;
        let hightmax = maxlines*maxh;
        if(h>hightmax)
        {
            
            return {fontsize, maxh}
        }
        fontsize--;
    }
}

function render(array){
    
    ctx.clearRect(0,0, 1920,1080);
    dowabck();
    ctx.fillStyle = "#ffffff";
    ctx.textBaseline = 'middle'
    
    // let textjson = [
    //     "بياا",
    //     "সুরু করলাম",
    //     "142:121",
    //     "ঋদৃুাকিদত ‍ুৃহাি afdajsfi (a)"
    // ]

    let textjson = array;
    
    ctx.font = 'bold 54px me_quran1';
    let fonth = getfontSizeFrame(textjson[0], 1750, 280, "me_quran1")

    ctx.textAlign = "end";
    wrapText(ctx, textjson[0], 1850, 170, 1750, fonth.maxh);

    ctx.textAlign = "center";
    ctx.font = 'bold 54px kalpurush';
    
    fonth = getfontSizeFrame(textjson[1], 1750, 280, "kalpurush")

    wrapText(ctx, textjson[1], 950, 630, 1750, fonth.maxh);
    ctx.textAlign = "start";
    ctx.font = 'bold 54px kalpurush'

    textw=ctx.measureText(textjson[2]).width;
    ctx.globalAlpha = 0.7;
    // #rect28
    ctx.beginPath();
    ctx.fillStyle = 'rgb(0, 175, 125)';
    ctx.rect(1705, 970, textw+24, 80);
    ctx.fill();
    textw=ctx.measureText(textjson[3]).width;
    // #rect26
    ctx.beginPath();
    ctx.fillStyle = 'rgb(0, 175, 125)';
    ctx.rect(63, 2.5, textw+24, 80);
    ctx.fill();

    ctx.globalAlpha = 1;
    
    
    ctx.fillStyle = "#ffffff";
    ctx.fillText(textjson[2] , 1720, 1010);
    ctx.fillText(textjson[3] , 70, 40);
}


appse = express()
appse.use(express.json());

appse.get("/", (req,res)=>{
    render(["مرحبًا بك في منشئ اللوحات القماشية","ক্যানভাস জেনারেটরে স্বাগতম", "000:000", "Welcome to the canvas generator"]);
    res.type("image/png");
    res.end(canvas.toBuffer("image/png"));
})
appse.post("/", (req, res)=>{
    render(req.body);
    res.type("image/png");
    res.end(canvas.toBuffer("image/png"));
})


appse.listen(8000, ()=>{
    console.log("server listen on 8000");
})

// fs.writeFileSync("image.png", );