from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

topic_analysis_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are an expert educator creating engaging micro-learning content.
            Analyze topics to create structured learning paths that are both educational and entertaining."""),
    HumanMessage(content="""
            Analyze this topic: {topic}
            
            Create a learning structure with:
            1. 5-7 core concepts (ordered from basic to advanced)
            2. Common misconceptions to address
            3. Real-world hooks to make it engaging
            
            Format as JSON:
            {{
                "concepts": ["concept1", "concept2", ...],
                "hooks": ["interesting fact", "surprising application", ...],
                "misconceptions": ["myth1", "myth2", ...],
                "prerequisites": ["prereq1", "prereq2", ...],
                "difficulty_range": {{"min": 1, "max": 5}}
            }}
            """)
])


qa_generation_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a TikTok-style educator creating snappy, engaging Q&A cards.
            
            CRITICAL RULES:
            - Questions: MAX 80 characters, intriguing, specific
            - Answers: MAX 150 characters, MUST use markdown formatting
            - Style: Engaging, surprising, "did you know?" vibe
            - No explanations - just punchy Q&A
            - Each card teaches ONE micro-concept
            
            Markdown formatting for answers:
            - **bold** for emphasis
            - `code` for technical terms
            - Lists with - or * 
            - ```lang for code blocks
            
            Make learning addictive!"""),

    HumanMessage(content="""
            Topic: {topic}
            Concepts to cover: {concepts}
            
            Previous questions (NEVER repeat these):
            {previous_questions}
            
            Generate {count} Q&A cards that:
            1. Build on each other progressively
            2. Are engaging and memorable
            3. Use varied question types (what/why/how/when)
            4. Include surprising facts or applications
            
            {format_instructions}
            """)
])
