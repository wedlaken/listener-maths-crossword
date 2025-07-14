# CS50 Final Project Video Script
## Listener Maths Crossword Solver

### Opening (15 seconds)
*[Display on screen]*
- **Project Title:** Listener Maths Crossword Solver
- **Name:** Neil Wedlake
- **GitHub:** wedlaken
- **edX:** [nwedlake
- **Location:** [London, United Kingdom
- **Date:** [12 July 2025

### Introduction (1 minute)
"Hi, I'm Neil Wedlake, and this is my CS50 final project. It is a sophisticated mathematical crossword solver that has evolved to incorporate multiple programming languages, frameworks,  and methodologies, using the latest iteration of coding aids. I've started several 'final' projects over the time since I started this CS50 course a couple of years ago as I felt that the programming environment was changing around me, and I wanted to learn how I would code in the future, rather than using rapidly outmoded approaches. 

According to the final project guidance for CS50 Introduction to Computer Science, AI copilots and similar aids can be used if they enhance the student's work and learning. If the guidance was written even a few months ago, it is likely that the current capability of copilots was underestimated. I have found that developing my project with Cursor AI as a guide has led me to learn vastly more, create a much more sophisiticated project and delve into areas of programming and functionality that I would not have had the time or patience to explore. 

I have used the AI tool to document the project development extensively, meticulously comment the code itself, and to record learning points for me to revisit - referenced to the functionality of the project and its code. I've been able to spend more time learning than laboriously styling in html and css or applying event listeners, for example. Instead, I've added database persistence, user authentication and other dimensions to the project.

What started as a simple puzzle solver has become a full-stack web application with real-time interactivity, user authentication, and advanced constraint satisfaction algorithms. I'm tremendously proud of what I've created with the appropriate tools, of what I have learnt, and of how I have gained experience of how coding is done intelligently with new technologies."

*[Show file structure and code examples]*

### Live Demo: Core Functionality (60 seconds)
*[Screen recording of the application – with inset video of me?]*

"Let me first show you the original newspaper puzzle that gave me the inspiration, and then demonstrate the solver in action.

The 'Listener Crossword' has a long and rich history in the Times newspaper – the London version – and is known to be very challenging. I did not realise at first that the nature of the puzzle is different each time it is published (every 3 months), and so my original idea, which was to design an application to recognise the puzzle grid and clues from camera shots, became redendant. I stopped trying to make OCR – visual recognition – work and expanded my work on the core logic and user interface.

The clues to the puzzle's first stage come as 2 numbers, the first being the number of prime factors in the solution, and the second is the difference between the largest and the smallest values. This can produce a large solution set for clues, although some turn out to be simply quadratics or factors of two, for example. I developed algorithms to constrain solution sets to account for solutions that intersect each other. The clues become class objects containing attributes such as their cell positions, sets of potential solutions and solved status and having methods that change those sets and states. The puzzle itself is an object that allows its state to be examined, saved and reloaded. The project has object oriented programming at its heart and is fully documented from a technical perspective in the various markdown documents in the 'docs' folder.

Four 'unclued clues' in the centre of the grid do not have the same clue type, but are numbers that are both multiples and anagrams of themselves. The final stage of the puzzle is to produce a grid that contains the digits in each initial grid solution in a different order (i.e. anagrams) with no conflicts where clues meet."

"Here's the interactive interface where users can:

1. **Select solutions** from computed possibilities
2. **See real-time constraint propagation** - when I choose a solution, incompatible options are automatically filtered out
3. **Use the undo system** - complete solution history with selective restoration
4. **Experience the anagram stage** - after completing the initial puzzle, users face a second challenge where every entry must be an anagram of the original
5. **Use development tools** - in order to speed up testing and development, I've added buttons to speed through the first level while maintaining its function

Notice the color coding: blue for user-selected solutions, green for algorithm-determined ones, and yellow for multiple possibilities."

### Technical Architecture (30 seconds)
*[Show key files and explain structure]*

"The application combines multiple programming paradigms:
- **Flask backend** with use of SQLAlchemy to make Python management programatic
- **Interactive JavaScript frontend** with real-time updates using the sophisticated clue objects
- **Mathematical algorithms** for prime factorization and constraint satisfaction
- **Database persistence** for cross-device progress synchronization

Each component demonstrates different CS50 concepts, from basic web development to advanced algorithmic thinking."

### Learning Outcomes & AI Collaboration (30 seconds)
*[Show documentation and learning points]*

"Working with Cursor taught me something crucial about modern development: AI isn't just about writing code faster - it's about thinking bigger. I could focus on architectural decisions, user experience design, and learning new technologies rather than getting stuck on syntax details.

I asked the AI to document the learning journey, creating comprehensive documentation that captures not just what we built, but why we made certain decisions and how we overcame challenges. This made hand over between AI sessions more or less seamless, which is analogous to how good documentation makes collaboration between human indiviuals and teams possible and effective. I also found the AI to be tireless and a lot better at commenting code through the project files, helping anyone who wants to quickly understand the code."

### Conclusion (15 seconds)
"This project demonstrates that with the right tools and mindset, you can build applications that go far beyond the first basic idea. The combination of human creativity and AI assistance allowed me to explore advanced programming concepts while creating something genuinely useful and educational. I hope you have fun playing the puzzle and looking around the codebase and the extensive .md documentation to see how the project developed, the challenges we overcame, changes of direction we took, and to see what else I'll be working on to improve and advance it further.

Thank you for watching!"

---

## Video Production Notes

### Visual Elements to Include:
1. **Opening slide** with project details
2. **File structure** showing the comprehensive codebase
3. **Live demo** of the interactive solver
4. **Code snippets** highlighting key features
5. **Documentation screenshots** showing learning points
6. **Original puzzle images** for context

### Key Messages to Emphasize:
- AI-assisted development expanded project scope significantly
- Focus shifted from syntax to architecture and user experience
- Demonstrated advanced programming concepts beyond CS50 requirements
- Created a production-ready application with real-world complexity
- Showed strategic thinking in development approach

### Timing Breakdown:
- Opening: 15 seconds
- Introduction: 30 seconds  
- AI Collaboration: 30 seconds
- Live Demo: 30 seconds
- Technical Overview: 30 seconds
- Learning Outcomes: 20 seconds
- Conclusion: 10 seconds
- **Total: <3 minutes** 