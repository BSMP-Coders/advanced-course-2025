document.addEventListener("DOMContentLoaded", function() {  
    const canvas = document.getElementById('gameCanvas');  
    const ctx = canvas.getContext('2d');  
  
    let bird = { x: 50, y: 150, width: 20, height: 20, gravity: 0.4, lift: -10, velocity: 0 }; // Reduce gravity  
    let pipes = [];  
    let score = 0;  
    let frame = 0;  
    const pipeWidth = 40;  
    const pipeGap = 200; // Increase pipe gap  
  
    function drawBird() {  
        ctx.fillStyle = "#fff";  
        ctx.fillRect(bird.x, bird.y, bird.width, bird.height);  
    }  
  
    function drawPipes() {  
        ctx.fillStyle = "#fff";  
        pipes.forEach(pipe => {  
            ctx.fillRect(pipe.x, pipe.top, pipeWidth, pipe.topHeight);  
            ctx.fillRect(pipe.x, pipe.bottom, pipeWidth, pipe.bottomHeight);  
        });  
    }  
  
    function updateBird() {  
        bird.velocity += bird.gravity;  
        bird.y += bird.velocity;  
  
        if (bird.y + bird.height > canvas.height || bird.y < 0) {  
            resetGame();  
        }  
    }  
  
    function updatePipes() {  
        if (frame % 100 === 0) { // Adjust frame interval for pipe generation  
            let topHeight = Math.floor(Math.random() * (canvas.height / 2));  
            let bottomHeight = canvas.height - topHeight - pipeGap;  
            pipes.push({  
                x: canvas.width,  
                top: 0,  
                topHeight: topHeight,  
                bottom: canvas.height - bottomHeight,  
                bottomHeight: bottomHeight  
            });  
        }  
  
        pipes.forEach(pipe => {  
            pipe.x -= 1.5; // Reduce pipe speed  
            if (pipe.x + pipeWidth < 0) {  
                pipes.shift();  
                score++;  
            }  
        });  
    }  
  
    function checkCollision() {  
        pipes.forEach(pipe => {  
            if (bird.x < pipe.x + pipeWidth && bird.x + bird.width > pipe.x &&  
                (bird.y < pipe.topHeight || bird.y + bird.height > pipe.bottom)) {  
                resetGame();  
            }  
        });  
    }  
  
    function resetGame() {  
        bird.y = 150;  
        bird.velocity = 0;  
        pipes = [];  
        score = 0;  
        frame = 0;  
    }  
  
    function drawScore() {  
        ctx.fillStyle = "#fff";  
        ctx.font = "20px Arial";  
        ctx.fillText("Score: " + score, 10, 20);  
    }  
  
    function gameLoop() {  
        ctx.clearRect(0, 0, canvas.width, canvas.height);  
        drawBird();  
        drawPipes();  
        drawScore();  
        updateBird();  
        updatePipes();  
        checkCollision();  
  
        frame++;  
        requestAnimationFrame(gameLoop);  
    }  
  
    document.addEventListener('keydown', function(e) {  
        if (e.code === 'Space') {  
            bird.velocity = bird.lift;  
        }  
    });  
  
    gameLoop();  
});  
