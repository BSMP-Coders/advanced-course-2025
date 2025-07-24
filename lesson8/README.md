# 📘 Lesson 8: Storytelling with Azure AI & Sora <!-- {docsify-ignore-all} -->

> [!NOTE] 
> 
> Refer to BSMP Coders Web Page for full lesson details here 👉 [Lesson 8: Storytelling with Azure AI & Sora](https://bsmp-coders.github.io/#/2025/adv/lesson8/lesson8)



### 📍 Introduction  
Welcome to Lesson 8! In this session, we explore how to use Azure AI Foundry and OpenAI’s Sora model to create compelling AI-generated video stories. This lesson builds on the storytelling foundations from Lesson 7 and introduces advanced prompt engineering for video generation.

> [!NOTE] Earn a digital badge by completing this assignment 
> [Microsoft Learn Module - Animate Images with Sora](https://learn.microsoft.com/en-us/training/modules/animate-impossible/?source=recommendations)



### What Is OpenAI's Sora? How It Works, Examples, Features

* What is it?: OpenAI Sora is a cool AI tool that creates videos from text or images, like turning "a sunflower opening" into a short video!
* How it helps: It’s used for making creative videos, animations, or even learning tools without needing fancy equipment.
* Fun Fact: It’s like a magic wand for video creation, powered by smart technology from OpenAI.

![](/../../../_media/v25/lesson8/sora_llamas.png)



<!--
<video controls style="width:100%; height:auto;">
    <source src="https://youtu.be/vLCqSUUOmy0" type="video/mp4">
    Your browser does not support the video tag.
</video>

<iframe width="560" height="315" src="https://youtu.be/vLCqSUUOmy0?si=AfCle6Dy9b4V80Ti" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
-->


#### Use reference images to generate videos
You can bring images to life by using the image-to-video capability that Veo has and use your existing assets or Imagen to generate something new.

| Description                  | Image/GIF                                                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------------------------|
| Bunny with a chocolate candy bar | ![Bunny with chocolate](https://cloud.google.com/static/vertex-ai/generative-ai/docs/video/images/static_bunny.png) |
| Bunny runs away              | ![Bunny running away](https://cloud.google.com/static/vertex-ai/generative-ai/docs/video/images/bunny_runs_away.gif)    |


---

### 🗂️ Agenda  
1. [Introduction to Azure AI Foundry & Sora](https://bsmp-coders.github.io/#/2025/adv/lesson8/lesson8/sora_prompts.md)  
2. What Makes a Good Story Prompt  
3. Writing Effective Prompts for Video  
4. Using Sora to Generate AI Videos - [sora dogs in class demo](https://bsmp-coders.github.io/#/2025/adv/lesson8/lesson8/sora_dogs_demo.md)  
5. [In-Class Activity: Create Your Own AI for Good Video](https://bsmp-coders.github.io/#/2025/adv/lesson8/lesson8/demo.md)  
6. Share & Reflect  

---

### 🧠 Key Concepts  
- Prompt Engineering for Video  
- Story Structure (Beginning, Middle, End, Message)  
- Visual & Emotional Detail in Prompts  
- AI for Good Themes  
- Using Azure AI Foundry Playgrounds  

<details>
<summary>Aditional Resources on Azure AI Foundry</summary>

  * [What is Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
  * [Video Generation - Quickstart](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/video-generation-quickstart)
  * [Image Generation - Quickstart](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/dall-e-quickstart)
</details>

---

### 🛠️ Tools Used  
- Azure AI Foundry (Sora Video Playground)  
- Microsoft Copilot Create  
- Clipchamp (optional for editing)  

---

### 🧪 In-Class Activity  
**Objective:** Create a short AI-generated video using Sora based on a structured storyboard prompt.

**Steps:**  
1. Brainstorm an “AI for Good” idea  
2. Write a storyboard prompt using the template  
3. Use Sora to generate a video from your prompt  
4. (Optional) Edit in Clipchamp  
5. Share your story with the class  

**Prompt Template:**  
```
Title: [Name + emoji]  
Concept: [1–2 sentence idea]  
Beginning: [Setting + problem]  
Middle: [How AI helps]  
End: [Outcome + who benefits]  
Message: [What does this say about AI?]  
```

---

### 🧵 Example Prompt  
**Title:** 🐆 Running Snow Leopard  
**Concept:** A joyful AI-generated winter scene featuring a snow leopard.  
**Beginning:** A snowy forest with falling snowflakes.  
**Middle:** A snow leopard prances through the trees.  
**End:** The leopard pauses, looks up at the sun.  
**Message:** AI can bring joy and wonder to storytelling.
