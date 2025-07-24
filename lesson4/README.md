# Rock Paper Scissors: Learning Python, Copilot, and Pygame

Welcome! In this lesson, you'll learn how to use GitHub Copilot to build Rock Paper Scissors games in Python, from a simple web recap to command-line and graphical versions using Pygame.

---

## Recap: Web Version with `python -m http.server`

_Last session, we learned how to use GitHub Copilot to generate web apps._

### Activity: Run a Simple Web Rock Paper Scissors

**File:** `1_web_recap.html`

1. **Prompt Copilot:**  
   _"Generate a basic HTML/JavaScript Rock Paper Scissors game with three buttons and a result display."_

2. **How to Run:**
   - Save the file as `1_web_recap.html`.
   - In your dev container terminal, run:
     ```bash
     python -m http.server
     ```
   - Open your browser to `http://localhost:8000/1_web_recap.html`.

---

## In-Class Activity 1: Command-Line Rock Paper Scissors

**File:** `2_basic_py.py`

1. **Prompt Copilot:**  
   _"Write a simple command-line Rock Paper Scissors game in Python. The user types their choice, the computer picks randomly, and the winner is printed. Add a way to quit."_

2. **How to Run:**
   - Save as `2_basic_py.py`.
   - Run in terminal:
     ```bash
     python 2_basic_py.py
     ```

---

## In-Class Activity 2: Introduction to Pygame

- [Pygame Tutorial](https://coderslegacy.com/python/python-pygame-tutorial/)
- [Pygame Official Tutorials](https://www.pygame.org/wiki/tutorials)

**Pygame Concepts:**
- Pygame is a library for making games in Python.
- You create a window, draw graphics, and handle user input.
- The main loop updates the screen and checks for events.

**Important:**  
For all Pygame activities in the dev container, add these lines at the top of your file:
```python
import os
os.environ["DISPLAY"] = ":1"
# or run DISPLAY=:1 python main.py 
```

**File:** `3_pygame_simple.py`

1. **Prompt Copilot:**  
   _"Create a very simple Rock Paper Scissors game using Pygame. Show three buttons, let the user click one, and display the result. No scores needed."_

2. **How to Run:**
   - Save as `3_pygame_simple.py`.
   - Run in terminal:
     ```bash
     python 3_pygame_simple.py
     ```

3. **Activity Ideas:**
   - Change button colors.
   - Add images or emojis.
   - Show a message for each result.

---

## In-Class Activity 3: Full Pygame Rock Paper Scissors

**File:** `4_pygame_full.py`

1. **Prompt Copilot:**  
   _"Build a complete Rock Paper Scissors game in Pygame with scores, reset button, and result display. Use classes and organize the code."_

2. **How to Run:**
   - Save as `4_pygame_full.py`.
   - Run in terminal:
     ```bash
     python 4_pygame_full.py
     ```

3. **Activity Ideas:**
   - Add sound effects.
   - Animate the buttons.
   - Keep a high score.

---

## Challenge: Make It Your Own!

- Use Copilot to iterate and make the game harder (e.g., add a timer, best-of-5, or AI).
- Or, try building a new game! For example, see the demo file `lesson5_space_invaders.py` for a simple Space Invaders using Pygame.

**Prompt Copilot:**  
_"Show me how to make a simple Space Invaders game in Pygame with a player, enemies, and shooting."_

---

## Tips for Using Copilot

- Start with a clear comment or docstring describing what you want.
- Accept, edit, or reject Copilot’s suggestions as needed.
- Experiment! Try changing prompts to see different results.

---

## Summary

- **Recap:** Web version with `python -m http.server`
- **Activity 1:** Command-line Python game
- **Activity 2:** Simple Pygame version
- **Activity 3:** Full-featured Pygame game
- **Challenge:** Iterate or build your own game

Happy coding and have fun with Copilot and