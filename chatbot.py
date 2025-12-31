"""
Chatbot Module - AI-Driven Conversational Agent.
Maintains conversation history and generates contextual responses using Gemini Flash 2.5.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ai_client import GeminiAIClient
from sentiment import SentimentAnalyzer, SentimentResult


class ConversationRole(Enum):
    """Enum for conversation participant roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Data class for a conversation message."""
    role: ConversationRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    sentiment: Optional[SentimentResult] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "sentiment": self.sentiment.to_dict() if self.sentiment else None
        }


class ConversationState:
    """Tracks the state of the conversation."""
    
    def __init__(self):
        self.mood: str = "neutral"
        self.engagement_level: str = "normal"
        self.topics_discussed: List[str] = []
        self.sentiment_trend: str = "stable"
        self.last_emotion: str = "neutral"
    
    def update(self, sentiment_result: SentimentResult):
        """Update state based on new sentiment analysis."""
        self.mood = sentiment_result.sentiment
        self.last_emotion = sentiment_result.emotion
        
        # Update engagement based on emotion intensity
        if sentiment_result.emotion_intensity == "high":
            self.engagement_level = "high"
        elif sentiment_result.emotion_intensity == "low":
            self.engagement_level = "low"
        else:
            self.engagement_level = "normal"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mood": self.mood,
            "engagement_level": self.engagement_level,
            "topics_discussed": self.topics_discussed,
            "sentiment_trend": self.sentiment_trend,
            "last_emotion": self.last_emotion
        }


class Chatbot:
    """
    AI-driven chatbot using Google Gemini Flash 2.5.
    Features:
    - Contextual response generation
    - Sentiment-aware replies
    - Conversation history management
    - Mood tracking and adaptation
    """
    
    def __init__(self, ai_client: GeminiAIClient = None, system_prompt: str = None):
        """
        Initialize the chatbot.
        
        Args:
            ai_client: Optional custom AI client
            system_prompt: Optional system prompt to set chatbot personality
        """
        self.ai_client = ai_client or GeminiAIClient()
        self.sentiment_analyzer = SentimentAnalyzer(self.ai_client)
        self.history: List[Message] = []
        self.state = ConversationState()
        
        # Set default system prompt if not provided
        self.system_prompt = system_prompt or (
            "You are a friendly, intelligent AI assistant. "
            "You are empathetic, helpful, and adapt your communication style "
            "based on the user's emotional state."
        )
        
        # Add system message
        self._add_system_message(self.system_prompt)
    
    def _add_system_message(self, content: str):
        """Add a system message to history."""
        message = Message(
            role=ConversationRole.SYSTEM,
            content=content
        )
        self.history.append(message)
    
    def _add_message(self, role: ConversationRole, content: str, 
                     sentiment: SentimentResult = None) -> Message:
        """Add a message to history."""
        message = Message(
            role=role,
            content=content,
            sentiment=sentiment
        )
        self.history.append(message)
        return message
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message and generate a response.
        
        Args:
            user_message: The user's input
            
        Returns:
            Dictionary containing response and analysis
        """
        # Step 1: Analyze user message sentiment
        sentiment_result = self.sentiment_analyzer.analyze(user_message)
        
        # Step 2: Update conversation state
        self.state.update(sentiment_result)
        
        # Step 3: Add user message to history
        self._add_message(
            ConversationRole.USER, 
            user_message, 
            sentiment_result
        )
        
        # Step 4: Generate contextual response
        response = self._generate_response(user_message, sentiment_result)
        
        # Step 5: Add assistant response to history
        self._add_message(ConversationRole.ASSISTANT, response)
        
        return {
            "response": response,
            "sentiment": sentiment_result.to_dict(),
            "state": self.state.to_dict(),
            "mood_context": self._get_mood_context()
        }
    
    def _generate_response(self, user_message: str, sentiment: SentimentResult) -> str:
        """Generate an AI response based on context and sentiment."""
        # Prepare conversation history for context
        history_for_ai = [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.history[-10:]  # Last 10 messages
        ]
        
        # Create sentiment context
        sentiment_context = (
            f"User sentiment: {sentiment.sentiment} | "
            f"Emotion: {sentiment.emotion} ({sentiment.emotion_intensity}) | "
            f"Reason: {sentiment.reasoning}"
        )
        
        # Generate response using AI
        response = self.ai_client.generate_reply(
            user_message=user_message,
            conversation_history=history_for_ai,
            current_mood=self.state.mood,
            sentiment_context=sentiment_context
        )
        
        return response.strip()
    
    def _get_mood_context(self) -> str:
        """Get current mood context as a string."""
        stats = self.sentiment_analyzer.get_summary_stats()
        
        return (
            f"Current mood: {self.state.mood} | "
            f"Emotion: {self.state.last_emotion} | "
            f"Engagement: {self.state.engagement_level} | "
            f"Messages: {stats['total_messages']}"
        )
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history as list of dicts."""
        return [msg.to_dict() for msg in self.history]
    
    def get_user_messages(self) -> List[str]:
        """Get all user messages."""
        return [
            msg.content for msg in self.history 
            if msg.role == ConversationRole.USER
        ]
    
    def get_sentiment_history(self) -> List[Dict[str, Any]]:
        """Get sentiment analysis history."""
        return self.sentiment_analyzer.get_history_dicts()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get AI-generated conversation summary."""
        history_for_summary = [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.history
            if msg.role != ConversationRole.SYSTEM
        ]
        
        return self.ai_client.summarize_conversation(history_for_summary)
    
    def get_keywords(self) -> Dict[str, Any]:
        """Get AI-extracted keywords from conversation."""
        history_for_keywords = [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.history
            if msg.role != ConversationRole.SYSTEM
        ]
        
        return self.ai_client.extract_keywords(history_for_keywords)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        user_msgs = sum(1 for m in self.history if m.role == ConversationRole.USER)
        assistant_msgs = sum(1 for m in self.history if m.role == ConversationRole.ASSISTANT)
        
        return {
            "total_messages": len(self.history) - 1,  # Exclude system message
            "user_messages": user_msgs,
            "assistant_messages": assistant_msgs,
            "sentiment_stats": self.sentiment_analyzer.get_summary_stats(),
            "conversation_state": self.state.to_dict()
        }
    
    def reset(self):
        """Reset the conversation."""
        self.history = []
        self.state = ConversationState()
        self.sentiment_analyzer.clear_history()
        self._add_system_message(self.system_prompt)
    
    def set_personality(self, personality: str):
        """
        Set a new personality for the chatbot.
        
        Args:
            personality: Description of the desired personality
        """
        self.system_prompt = personality
        # Update system message in history
        if self.history and self.history[0].role == ConversationRole.SYSTEM:
            self.history[0] = Message(
                role=ConversationRole.SYSTEM,
                content=personality
            )


class SmartChatbot(Chatbot):
    """
    Enhanced chatbot with additional AI-powered features.
    Includes mood-adaptive responses and proactive engagement.
    """
    
    def __init__(self, ai_client: GeminiAIClient = None):
        super().__init__(ai_client)
        self.mood_shift_threshold = 2  # Number of messages to detect mood shift
        self.previous_moods: List[str] = []
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Enhanced chat with mood shift detection."""
        result = super().chat(user_message)
        
        # Track mood for shift detection
        self.previous_moods.append(result["sentiment"]["sentiment"])
        
        # Detect mood shifts
        mood_shift = self._detect_mood_shift()
        result["mood_shift_detected"] = mood_shift
        
        # Add contextual hints for the UI
        result["ui_hints"] = self._generate_ui_hints(result["sentiment"])
        
        return result
    
    def _detect_mood_shift(self) -> Optional[Dict[str, str]]:
        """Detect significant mood shifts in the conversation."""
        if len(self.previous_moods) < self.mood_shift_threshold:
            return None
        
        recent = self.previous_moods[-self.mood_shift_threshold:]
        
        # Check if there's a consistent shift
        if len(set(recent)) == 1:
            return None  # No shift, mood is consistent
        
        # Detect direction of shift
        mood_values = {"positive": 1, "neutral": 0, "negative": -1}
        
        if len(recent) >= 2:
            prev_val = mood_values.get(recent[-2], 0)
            curr_val = mood_values.get(recent[-1], 0)
            
            if curr_val > prev_val:
                return {"direction": "improving", "from": recent[-2], "to": recent[-1]}
            elif curr_val < prev_val:
                return {"direction": "declining", "from": recent[-2], "to": recent[-1]}
        
        return None
    
    def _generate_ui_hints(self, sentiment: Dict) -> Dict[str, Any]:
        """Generate hints for UI display based on sentiment."""
        emotion = sentiment.get("emotion", "neutral")
        intensity = sentiment.get("emotion_intensity", "medium")
        
        # Color suggestions
        color_map = {
            "happy": "#4CAF50",
            "excited": "#FF9800",
            "sad": "#2196F3",
            "angry": "#F44336",
            "confused": "#9C27B0",
            "anxious": "#607D8B",
            "neutral": "#9E9E9E",
            "frustrated": "#E91E63",
            "hopeful": "#00BCD4",
            "surprised": "#FFEB3B"
        }
        
        # Icon suggestions
        icon_map = {
            "happy": "😊",
            "excited": "🎉",
            "sad": "😢",
            "angry": "😠",
            "confused": "😕",
            "anxious": "😰",
            "neutral": "😐",
            "frustrated": "😤",
            "hopeful": "🌟",
            "surprised": "😮"
        }
        
        return {
            "suggested_color": color_map.get(emotion, "#9E9E9E"),
            "emotion_icon": icon_map.get(emotion, "😐"),
            "intensity_level": {"low": 1, "medium": 2, "high": 3}.get(intensity, 2)
        }
