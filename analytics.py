"""
Analytics Module - AI-Powered Conversation Analytics.
Provides trend analysis, keyword extraction, and visualizations using Gemini Flash 2.5.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

from ai_client import GeminiAIClient


@dataclass
class TrendData:
    """Data class for trend analysis results."""
    trend: str  # improving, declining, stable, volatile
    direction: str  # positive, negative, neutral
    mood_shifts: List[str]
    emotional_peaks: List[str]
    analysis: str
    prediction: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trend": self.trend,
            "direction": self.direction,
            "mood_shifts": self.mood_shifts,
            "emotional_peaks": self.emotional_peaks,
            "analysis": self.analysis,
            "prediction": self.prediction
        }


class ConversationAnalytics:
    """
    AI-powered analytics for conversation data.
    All analysis is performed using Google Gemini Flash 2.5.
    """
    
    def __init__(self, ai_client: GeminiAIClient = None):
        """Initialize analytics with AI client."""
        self.ai_client = ai_client or GeminiAIClient()
    
    def analyze_trends(self, sentiment_history: List[Dict]) -> TrendData:
        """
        Analyze sentiment trends over the conversation.
        
        Args:
            sentiment_history: List of sentiment analysis results
            
        Returns:
            TrendData with comprehensive trend analysis
        """
        result = self.ai_client.generate_trend_analysis(sentiment_history)
        
        return TrendData(
            trend=result.get("trend", "stable"),
            direction=result.get("direction", "neutral"),
            mood_shifts=result.get("mood_shifts", []),
            emotional_peaks=result.get("emotional_peaks", []),
            analysis=result.get("analysis", "No analysis available."),
            prediction=result.get("prediction", "Unable to predict.")
        )
    
    def extract_keywords(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Extract keywords and themes from conversation.
        
        Args:
            conversation_history: Full conversation history
            
        Returns:
            Dictionary with keywords, themes, and analysis
        """
        return self.ai_client.extract_keywords(conversation_history)
    
    def get_summary(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Get comprehensive conversation summary.
        
        Args:
            conversation_history: Full conversation history
            
        Returns:
            Dictionary with summary and insights
        """
        return self.ai_client.summarize_conversation(conversation_history)
    
    def generate_mood_graph(self, sentiment_history: List[Dict]) -> str:
        """
        Generate ASCII mood graph using AI.
        
        Args:
            sentiment_history: List of sentiment analysis results
            
        Returns:
            ASCII art mood visualization
        """
        return self.ai_client.generate_ascii_mood_graph(sentiment_history)
    
    def generate_emotion_profile(self, sentiment_history: List[Dict]) -> str:
        """
        Generate comprehensive emotion profile.
        
        Args:
            sentiment_history: List of sentiment analysis results
            
        Returns:
            Detailed emotion profile text
        """
        return self.ai_client.generate_emotion_profile(sentiment_history)
    
    def get_full_report(self, conversation_history: List[Dict], 
                        sentiment_history: List[Dict]) -> Dict[str, Any]:
        """
        Generate a complete analytics report.
        
        Args:
            conversation_history: Full conversation history
            sentiment_history: List of sentiment analysis results
            
        Returns:
            Comprehensive analytics report
        """
        # Get all analytics
        trends = self.analyze_trends(sentiment_history)
        keywords = self.extract_keywords(conversation_history)
        summary = self.get_summary(conversation_history)
        mood_graph = self.generate_mood_graph(sentiment_history)
        emotion_profile = self.generate_emotion_profile(sentiment_history)
        
        # Calculate statistics
        stats = self._calculate_statistics(sentiment_history)
        
        return {
            "summary": summary,
            "trends": trends.to_dict(),
            "keywords": keywords,
            "statistics": stats,
            "mood_graph": mood_graph,
            "emotion_profile": emotion_profile
        }
    
    def _calculate_statistics(self, sentiment_history: List[Dict]) -> Dict[str, Any]:
        """Calculate basic statistics from sentiment history."""
        if not sentiment_history:
            return {
                "total_messages": 0,
                "sentiment_distribution": {},
                "emotion_distribution": {},
                "average_confidence": 0.0
            }
        
        # Count sentiments
        sentiment_dist = {}
        emotion_dist = {}
        total_confidence = 0.0
        
        for item in sentiment_history:
            # Sentiment distribution
            sentiment = item.get("sentiment", "neutral")
            sentiment_dist[sentiment] = sentiment_dist.get(sentiment, 0) + 1
            
            # Emotion distribution
            emotion = item.get("emotion", "neutral")
            emotion_dist[emotion] = emotion_dist.get(emotion, 0) + 1
            
            # Confidence
            total_confidence += float(item.get("confidence", 0.5))
        
        return {
            "total_messages": len(sentiment_history),
            "sentiment_distribution": sentiment_dist,
            "emotion_distribution": emotion_dist,
            "average_confidence": total_confidence / len(sentiment_history),
            "dominant_sentiment": max(sentiment_dist, key=sentiment_dist.get) if sentiment_dist else "neutral",
            "dominant_emotion": max(emotion_dist, key=emotion_dist.get) if emotion_dist else "neutral"
        }


class ReportGenerator:
    """
    Generates formatted reports from analytics data.
    """
    
    def __init__(self, analytics: ConversationAnalytics = None):
        """Initialize report generator."""
        self.analytics = analytics or ConversationAnalytics()
    
    def generate_text_report(self, conversation_history: List[Dict],
                             sentiment_history: List[Dict]) -> str:
        """
        Generate a formatted text report.
        
        Args:
            conversation_history: Full conversation history
            sentiment_history: List of sentiment analysis results
            
        Returns:
            Formatted text report
        """
        report = self.analytics.get_full_report(conversation_history, sentiment_history)
        
        lines = []
        lines.append("=" * 60)
        lines.append("           CONVERSATION ANALYTICS REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Summary Section
        lines.append("📊 CONVERSATION SUMMARY")
        lines.append("-" * 40)
        summary = report.get("summary", {})
        lines.append(f"Summary: {summary.get('summary', 'N/A')}")
        lines.append(f"Overall Tone: {summary.get('overall_tone', 'N/A')}")
        lines.append(f"Mood Journey: {summary.get('user_mood_journey', 'N/A')}")
        
        if summary.get("key_points"):
            lines.append("\nKey Points:")
            for point in summary.get("key_points", []):
                lines.append(f"  • {point}")
        
        lines.append("")
        
        # Trends Section
        lines.append("📈 SENTIMENT TRENDS")
        lines.append("-" * 40)
        trends = report.get("trends", {})
        lines.append(f"Trend: {trends.get('trend', 'N/A')}")
        lines.append(f"Direction: {trends.get('direction', 'N/A')}")
        lines.append(f"Analysis: {trends.get('analysis', 'N/A')}")
        lines.append(f"Prediction: {trends.get('prediction', 'N/A')}")
        
        if trends.get("mood_shifts"):
            lines.append("\nMood Shifts:")
            for shift in trends.get("mood_shifts", []):
                lines.append(f"  ↔ {shift}")
        
        lines.append("")
        
        # Keywords Section
        lines.append("🔑 KEYWORDS & THEMES")
        lines.append("-" * 40)
        keywords = report.get("keywords", {})
        
        if keywords.get("keywords"):
            lines.append(f"Keywords: {', '.join(keywords.get('keywords', []))}")
        
        if keywords.get("themes"):
            lines.append(f"Themes: {', '.join(keywords.get('themes', []))}")
        
        if keywords.get("topics_of_interest"):
            lines.append(f"Topics of Interest: {', '.join(keywords.get('topics_of_interest', []))}")
        
        lines.append("")
        
        # Statistics Section
        lines.append("📉 STATISTICS")
        lines.append("-" * 40)
        stats = report.get("statistics", {})
        lines.append(f"Total Messages Analyzed: {stats.get('total_messages', 0)}")
        lines.append(f"Average Confidence: {stats.get('average_confidence', 0):.1%}")
        lines.append(f"Dominant Sentiment: {stats.get('dominant_sentiment', 'N/A')}")
        lines.append(f"Dominant Emotion: {stats.get('dominant_emotion', 'N/A')}")
        
        sentiment_dist = stats.get("sentiment_distribution", {})
        if sentiment_dist:
            lines.append("\nSentiment Distribution:")
            for sentiment, count in sentiment_dist.items():
                lines.append(f"  {sentiment.capitalize()}: {count}")
        
        emotion_dist = stats.get("emotion_distribution", {})
        if emotion_dist:
            lines.append("\nEmotion Distribution:")
            for emotion, count in sorted(emotion_dist.items(), key=lambda x: -x[1])[:5]:
                lines.append(f"  {emotion.capitalize()}: {count}")
        
        lines.append("")
        
        # Mood Graph Section
        lines.append("📊 MOOD VISUALIZATION")
        lines.append("-" * 40)
        lines.append(report.get("mood_graph", "No visualization available."))
        lines.append("")
        
        # Emotion Profile Section
        lines.append("🎭 EMOTION PROFILE")
        lines.append("-" * 40)
        lines.append(report.get("emotion_profile", "No profile available."))
        lines.append("")
        
        lines.append("=" * 60)
        lines.append("           END OF REPORT")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def generate_json_report(self, conversation_history: List[Dict],
                             sentiment_history: List[Dict]) -> Dict[str, Any]:
        """
        Generate a JSON-formatted report.
        
        Args:
            conversation_history: Full conversation history
            sentiment_history: List of sentiment analysis results
            
        Returns:
            Dictionary report suitable for JSON serialization
        """
        return self.analytics.get_full_report(conversation_history, sentiment_history)


def create_simple_ascii_graph(values: List[float], width: int = 50, height: int = 10) -> str:
    """
    Create a simple ASCII graph from numeric values.
    This is a fallback function - the main graph is AI-generated.
    
    Args:
        values: List of numeric values (0.0 to 1.0 scale)
        width: Width of the graph
        height: Height of the graph
        
    Returns:
        ASCII graph string
    """
    if not values:
        return "No data to display."
    
    # Normalize values to height
    max_val = max(values) if max(values) > 0 else 1
    min_val = min(values) if min(values) < max_val else 0
    range_val = max_val - min_val if max_val != min_val else 1
    
    normalized = [(v - min_val) / range_val for v in values]
    
    # Create graph
    lines = []
    
    for row in range(height, -1, -1):
        threshold = row / height
        line = "│"
        for val in normalized:
            if val >= threshold:
                line += "█"
            else:
                line += " "
        lines.append(line)
    
    # Add x-axis
    lines.append("└" + "─" * len(values))
    
    return "\n".join(lines)
